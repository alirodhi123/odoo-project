# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

import subprocess
import odoo.addons.decimal_precision as dp



class sale_custom(models.Model):
     _inherit = 'mrp.workorder'

     x_prod_temp = fields.Many2one('product.template',related = 'product_id.product_tmpl_id')
     x_layout_product = fields.One2many(related = 'x_prod_temp.x_layout_product_ids')
     # x_type_lebaran = fields.Selection(related='x_layout_product.x_type', domain = [('x_layout_product.x_type', '=', 'Arround')])
     x_lebaran_bahan = fields.Float(string = 'lebar', related = 'x_layout_product.x_jumlah')
     x_qty_meter = fields.Float(string = 'Meter')
     x_jml_prod = fields.Integer(string = 'jumlah Product')
     x_lot_operation = fields.One2many('x.lot.operation', 'x_routing_process', string = 'Lot Operation')
     x_time_idsduration = fields.Float(string = 'duration total')
     x_ids_duration = fields.Float(related = 'time_ids.duration')
     x_total_duration = fields.Float(string = 'Total Durasi')
     x_shift_leader = fields.Many2one('hr.employee', string='Shift Leader')
     # CALENDAR
     date_planned_start = fields.Datetime(
         'Scheduled Date Start',
         states={'done': [('readonly', True)], 'cancel': [('readonly', True)]})
     date_planned_finished = fields.Datetime(
         'Scheduled Date Finished',
         states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
         compute='create_date_planned_finished')
     # CUSTOM
     custom_move_lot_ids = fields.One2many('x.move.lots', 'workorder_id')


     @api.onchange('x_qty_meter')
     def meter_to_pcs(self):
          self.x_jml_prod = 0
          for x in self.x_layout_product:
               self.x_jml_prod = self.x_jml_prod + x.x_number
               if x.x_type == 'arround':
                    self.x_lebaran_bahan = x.x_jumlah / 1000
               self.qty_producing = int((self.x_qty_meter * self.x_jml_prod) / self.x_lebaran_bahan)

     @api.onchange ('x_ids_duration')
     def duration_real(self):
          self.duration = self.duration + self.x_ids_duration

     # Function Get Lot pada OK
     @api.multi
     def generate_lot_reference(self):
         for workorder in self:
             workorder.delete_generate_lot_action()
             workorder.generate_lot_reference_action()


     # Function untuk Generate lot reference
     @api.multi
     def generate_lot_reference_action(self):
        lot_ids = []
        production_id = self.production_id
        stock_move_lots = self.env['stock.move.lots']
        stock_production_lot = self.env['stock.production.lot']
        production = self.env['mrp.production'].search([('id', '=', production_id.id)])
        if production:
            for row in production.move_raw_ids:
                product = row.product_id
                product_stock = stock_move_lots.search([('product_id', '=', product.id),
                                                        ('production_id', '=', production_id.id)])
                if product_stock:
                    lot_temp = ""
                    for o in product_stock:
                        lot_id = o.lot_id

                        coba = stock_production_lot.search([('product_id', '=', product.id),
                                                            ('id', '=', lot_id.id)])
                        if coba:
                            for lot in coba:
                                if product.id == o.product_id.id:
                                    if lot_temp:
                                        lot_temp += ", " + lot.name
                                    else:
                                        lot_temp = lot.name

                    # Insert ke dalam one2many field
                    if lot_temp:
                        values = {}
                        values['x_product_id'] = product
                        values['x_lot'] = lot_temp
                        lot_ids.append((0, 0, values))

        self.update({'custom_move_lot_ids': lot_ids})

        # Setelah itu parsing lot ke tab Current Production
        self.generate_lot_update_action()


     # Setelah dimasukkan ke dalam tampungan sementara,
     # akan di parsing lagi ke lot reference pada tab Current Prooduction
     @api.multi
     def generate_lot_update_action(self):
         lot_ids = []
         production_id = self.production_id

         production = self.env['x.move.lots'].search([('workorder_id', '=', self.id)])
         if production:
             for row in production:
                 to_consume = row.x_lot
                 product_id = row.x_product_id.id

                 move_lots = self.env['stock.move.lots'].search([('workorder_id', '=', self.id),
                                                                 ('production_id', '=', production_id.id)])
                 for o in move_lots:
                     id = o.id
                     move_product = o.product_id

                     if product_id == move_product.id:
                         values = {}
                         values['x_lot_reference'] = to_consume
                         # Update existing record berdasarkan product
                         lot_ids.append((1, id, values))

             return self.update({'active_move_lot_ids': lot_ids})


     @api.multi
     def delete_generate_lot_action(self):
         generate_lot_ids = []
         workorder_id = self.id

         x_move_lots = self.env['x.move.lots'].search([('workorder_id', '=', workorder_id)])
         if x_move_lots:
             for line in x_move_lots:
                 generate_lot_ids.append(([5]))

             return self.update({'custom_move_lot_ids': generate_lot_ids})

     # Perhitungan tanggal start date + expected duration WO
     @api.one
     def create_date_planned_finished(self):
         start_date = self.date_planned_start
         if start_date != False:
             format = "%Y-%m-%d %H:%M:%S"
             start_date_var = datetime.strptime(str(start_date), format)
             self.date_planned_finished = start_date_var + relativedelta(hours=float(self.duration_expected / 60))



class lot_operation(models.Model):
     _name = 'x.lot.operation'

     x_routing_process = fields.Many2one('mrp.workorder', string='Routing Proses')
     x_user = fields.Many2one('res.partner', string='Operator')
     x_routing = fields.Many2one('mrp.workorder', string='Routing Proses')
     name = fields.Many2one('stock.production.lot', string='Nomor Lot')


class mrp_inherit(models.Model):
    _inherit = 'mrp.workcenter.productivity'

    # user_id = fields.Many2one('hr.employee', string='User 1')
    x_wo_rp = fields.Many2one('mrp.workorder', string='Routing Proses')
    x_kd_mesin = fields.Char(string = 'Kode Mesin')
    x_user = fields.Many2one('hr.employee', string='User 1')
    x_wo_user2 = fields.Many2one('hr.employee', string='User 2')
    x_leader = fields.Many2one('hr.employee', string='Shift Leader')
    x_wo_lot = fields.Char(string='Nomor Lot')
    x_keterangan = fields.Text(string="Keterangan")
    x_qty = fields.Float(string="Qty")
    # x_total_qty = fields.Float()
    # x_shift_leader = fields.Many2one('hr.employee', string='Shift Leader')

    # @api.onchange('x_qty')
    # def total_qty(self):
    #     self.x_total_qty = 0
    #     for x in self.time_ids:
    #         self.x_total_qty = self.x_total_qty + x.x_qty




