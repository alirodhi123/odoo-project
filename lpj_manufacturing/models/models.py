# -*- coding: utf-8 -*-
import subprocess
from datetime import datetime
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp


class mrp_production(models.Model):
     _inherit = 'mrp.production'

     x_buffer_tags = fields.Many2many('buffer.tags', string="Material Location")
     x_tampungan_bu = fields.Text(compute='get_product_bu')
     production_id = fields.Char(string="OK Reference")
     panjang_bahan_bu = fields.Text()
     panjang_bahan_max = fields.Float()
     panjang_bahan_bu_tinta = fields.Char()
     panjang_bahan_laminating_tinta = fields.Char()
     panjang_bahan_pita_tinta = fields.Char()
     panjang_bahan_hot_foil_tinta = fields.Char()
     panjang_bahan_label_tinta = fields.Char()
     date_planned_start = fields.Datetime('Deadline Start', copy=False, default=fields.Datetime.now,index=True, required=True,
                          states={'confirmed': [('readonly', False)]}, oldname="date_planned", track_visibility='onchange')
     date_planned_finished = fields.Datetime('Deadline End', copy=False, index=True, states={'confirmed': [('readonly', False)]},
                                             compute='onchange_date_planned_finished')
     x_is_administrator = fields.Boolean(string="Is Administrator", default=False, compute='get_user_admin')
     x_tgl_produksi = fields.Date(string="Tanggal Turun Produksi")
     x_flag_produksi = fields.Boolean(default=False)
     purchase_request_count = fields.Integer(compute='_compute_purchase_req_count')
     x_manufacturing_type_ok = fields.Selection([('laprint', 'Laprint'), ('digital', 'Digital')],
                                             default='laprint', string="Manufacturing Type", readonly=True)
     x_planning_type_ok = fields.Selection([('forward', 'Forward Planning'), ('backward', 'Backward Planning')],
                                        default='forward', string="Planning Type", readonly=True)
     x_status_ok = fields.Selection([('urgent', 'Urgent'), ('not_urgent', 'Not Urgent')], default='not_urgent', string="Status OK")
     x_temp_mo = fields.Integer(readonly=True)
     x_qtytoproduce_temp = fields.Float()
     x_is_user_scm = fields.Boolean(default=False, compute='is_get_user')


    # Fungsi ketika save OK
    # -uswa-tambah ini
     @api.model
     def create(self, vals):

         type_mo = vals['x_type_mo']
         sale_order = vals['order']

         if type_mo == 'stc' and not sale_order:
             raise UserError(_(
                 'Please Insert SO Number to Continue Saving, Otherwise You Can Choose Type MO : Trial to Create OK Sticker without SO Number'))

         return super(mrp_production, self).create(vals)

     # WORKORDER
     # Fungsi ambil field finish date yang paling lama
     @api.one
     def onchange_date_planned_finished(self):
         raw_date = 0
         for data in self.workorder_ids:
             if data.date_planned_finished != False:
                 if data.date_planned_finished >= raw_date:
                     raw_date = data.date_planned_finished

         if raw_date != 0:
             self.date_planned_finished = raw_date


     # ORDER KERJA
     # Ambil data dari OK STICKER
     # Untuk Report OK NON STICKER
     @api.onchange('production_id')
     def get_order_kerja(self):
         id = self.production_id
         order_kerja = self.env['mrp.production'].search([('name', '=', id)])
         if order_kerja:
             bu = order_kerja.x_tampungan_bu
             panjang_bahan_max = order_kerja.x_product_uom_qty

             # Pindahkan ke variabel
             self.panjang_bahan_bu = bu
             self.panjang_bahan_max = panjang_bahan_max


     # REPORT
     # Get product BU yg ada di BOM dan tampilkan di report
     # Hanya BU SAJA
     @api.depends('move_raw_ids')
     def get_product_bu(self):
         for data in self:
             tampungan = ""
             for row in data.move_raw_ids:
                 category_utama = row.product_tmpl_id.categ_id.sts_bhn_utama.name

                 if category_utama == "Bahan Utama":
                     if tampungan:
                        tampungan = tampungan + ", " + row.product_id.display_name
                     else:
                        tampungan = row.product_id.display_name

             data.x_tampungan_bu = tampungan


     # MANUFACTURING ORDER
     # Function flagging admin untuk button cancel di OK
     @api.one
     def get_user_admin(self):
         for manufacturing in self:
             state = manufacturing.state
             uid = manufacturing._uid
             res_user = manufacturing.env['res.users'].search([('id', '=', manufacturing._uid)])
             # Jika state OK progress atau planned
             if state == "progress" or state == "planned":
                 # Jika login sebagai administrator atau bu nurul (43)
                 if res_user.has_group('base.group_system') or res_user.id == 43:
                     manufacturing.update({'x_is_administrator': True})
                 else:
                     manufacturing.update({'x_is_administrator': False})

             # Jika state OK confirmed
             elif state == "confirmed":
                 # Jika login tidak sebagai administrator
                 manufacturing.update({'x_is_administrator': True})
                 pass

     # Button turun produksi
     @api.multi
     def production(self):
         for production in self:
            default = datetime.now().strftime('%Y-%m-%d')
            production.update({
                'x_tgl_produksi': default,
                'x_flag_produksi': True
            })

     # Toggle button, function untuk membuka halaman purchase req
     @api.multi
     def purchase_req_view_action(self):
         action = self.env.ref('purchase_request.purchase_request_form_action').read()[0]
         action['domain'] = [('x_no_ok', '=', self.id)]
         action['context'] = {}
         return action

     # Function untuk menghitung jumlah PR
     @api.multi
     def _compute_purchase_req_count(self):
         for o in self:
             purchase_req_obj = self.env['purchase.request'].search([('x_no_ok', '=', o.id)])
             if purchase_req_obj:

                 log_purchase_data = purchase_req_obj.sudo().read_group([('x_no_ok', 'in', self.ids)],
                                                                          ['x_no_ok'],
                                                                          ['x_no_ok'])
                 result = dict(
                     (data['x_no_ok'][0], data['x_no_ok_count']) for data in log_purchase_data)
                 for purchase in self:
                     purchase.purchase_request_count = result.get(purchase.id, 0)

     # FUNCTION UPDATE QTY TO PRODUCE
     @api.multi
     def update_qty_produced(self):
         # Custom function ali
         type_mo = self.x_type_mo
         order = self.order
         sale_order_line_id = self.x_product_order_line
         mo_id = self.id
         x_qtytoproduce_temp = self.x_qtytoproduce_temp

         if type_mo == 'stc' and order and sale_order_line_id:
             sale_order_obj = self.env['sale.order'].search([('id', '=', order.id)])
             quantity_to_produce = self.product_qty
             product_ok = self.product_id

             if sale_order_obj:
                 for order_line in sale_order_obj.order_line:
                     product_so = order_line.product_id
                     ordered_qty = order_line.product_uom_qty

                     if product_so == product_ok:
                         # Jika masih dalam OK yang sama
                         if mo_id == self.x_temp_mo and quantity_to_produce <= x_qtytoproduce_temp:
                             temp_produced_ok = quantity_to_produce
                             qty_produced_so = order_line.x_qty_produced_ok

                             # Perhitungan
                             sementara = x_qtytoproduce_temp - temp_produced_ok
                             hasil = qty_produced_so - sementara

                             order_line.update({'x_qty_produced_ok': hasil})

                             self.x_temp_mo = mo_id
                             self.x_qtytoproduce_temp = temp_produced_ok

                             if order_line.x_qty_produced_ok >= ordered_qty:
                                 order_line.update({'x_flag_mo': True})

                             else:
                                 order_line.update({'x_flag_mo': False})

                         elif mo_id == self.x_temp_mo and quantity_to_produce > x_qtytoproduce_temp:
                             temp_produced_ok = quantity_to_produce
                             qty_produced_so = order_line.x_qty_produced_ok

                             # Perhitungan
                             sementara = temp_produced_ok - x_qtytoproduce_temp
                             hasil = qty_produced_so + sementara

                             order_line.update({'x_qty_produced_ok': hasil})

                             self.x_temp_mo = mo_id
                             self.x_qtytoproduce_temp = temp_produced_ok

                             if order_line.x_qty_produced_ok >= ordered_qty:
                                 order_line.update({'x_flag_mo': True})

                             else:
                                 order_line.update({'x_flag_mo': False})

                         else:

                             temp_produced_ok = quantity_to_produce + order_line.x_qty_produced_ok

                             order_line.update({'x_qty_produced_ok': temp_produced_ok})

                             self.x_temp_mo = mo_id
                             self.x_qtytoproduce_temp = quantity_to_produce

                             # Update flagging x_flag_mo jika produced qty >= ordered qty
                             if order_line.x_qty_produced_ok >= ordered_qty:
                                 order_line.update({'x_flag_mo': True})

                             else:
                                 order_line.update({'x_flag_mo': False})

     # INHERITE BUTTON CREATE WORKORDER
     @api.multi
     def button_plan(self):
         # FUNCTION UPDATE QTY TO PRODUCE
         self.update_qty_produced()

         res = super(mrp_production, self).button_plan()
         return res

     # Function update qty pproduced ketika di cancel
     @api.multi
     def update_qty_produced_cancel(self):
         type_mo = self.x_type_mo
         order = self.order
         sale_order_line_id = self.x_product_order_line

         if type_mo == 'stc' and order and sale_order_line_id:
             sale_order_obj = self.env['sale.order'].search([('id', '=', order.id)])
             quantity_to_produce = self.product_qty
             product_ok = self.product_id

             if sale_order_obj:
                 for order_line in sale_order_obj.order_line:
                     product_so = order_line.product_id

                     if product_so == product_ok:
                         quantity_to_produce_so = order_line.x_qty_produced_ok
                         if quantity_to_produce_so > quantity_to_produce:
                            hasil = quantity_to_produce_so - quantity_to_produce
                            order_line.update({'x_qty_produced_ok': hasil})

     # Fungsi Cancel WO
     @api.multi
     def action_cancel_wo(self):
         for row in self:
             workorder_obj = row.env['mrp.workorder'].search([('production_id', '=', row.id)])
             if workorder_obj:
                 for data in workorder_obj:
                    data.update({'state': 'cancel'})

                 return True

     # INHERITE BUTTON CREATE WORKORDER
     @api.multi
     def action_cancel(self):
         # FUNCTION UPDATE QTY TO PRODUCE
         self.update_qty_produced_cancel()
         self.action_cancel_wo()

         res = super(mrp_production, self).action_cancel()
         return res


     # Get user bu nurul
     @api.one
     def is_get_user(self):
         res_user = self.env['res.users'].search([('id', '=', self._uid)])
         if res_user:
             id = res_user.id
             # Jika yang login bu nurul
             if id == 43:
                 self.x_is_user_scm = True
             elif res_user.has_group('base.group_system'):
                 self.x_is_user_scm = True
             else:
                 self.x_is_user_scm = False

     # Fungsi cek qty ketika klik POST INVENTORY
     # Qty cetak >= qty packing maka error message
     @api.multi
     def cek_qty_cetak_wo(self):
         for production in self:
             type_mo = production.x_type_mo
             id_cetak_wo = 0
             id_packing_wo = 0
             qty_produced_wo_cetak = 0
             qty_produced_wo_packing = 0
             production_id = production.id

             if type_mo == 'stc':
                 workorder_obj = production.env['mrp.workorder'].search([('production_id', '=', production_id)])
                 if workorder_obj:
                     # Cari id cetak
                     self.env.cr.execute("select id from mrp_workorder where id = "
                                            "(select MIN(id) from mrp_workorder where production_id = '" + str(production_id) + "')")

                     cetak_id = self.env.cr.fetchone()
                     if cetak_id:
                         id_cetak_wo = cetak_id[0]

                     # Cari id Packing
                     self.env.cr.execute("select id from mrp_workorder where id = "
                                         "(select MAX(id) from mrp_workorder where production_id = '" + str(production_id) + "')")

                     packing_id = self.env.cr.fetchone()
                     if packing_id:
                         id_packing_wo = packing_id[0]

                     for row in workorder_obj:
                         if row.id == id_cetak_wo:
                            qty_produced_wo_cetak = row.qty_produced
                         elif row.id == id_packing_wo:
                             qty_produced_wo_packing = row.qty_produced
                         else:
                             pass

                     if qty_produced_wo_packing > qty_produced_wo_cetak or qty_produced_wo_packing <= 0:
                         raise UserError(_(
                             'Quantity printing can not be less than quantity packing'))

     # INHERITE BUTTON POST INVENTORY
     @api.multi
     def post_inventory(self):
         # FUNCTION CEK QTY CETAK DAN PACKING
         self.cek_qty_cetak_wo()

         res = super(mrp_production, self).post_inventory()
         return res












