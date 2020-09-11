# -*- coding: utf-8 -*-
import subprocess

from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from datetime import datetime
from odoo.exceptions import UserError


class lot_barang(models.Model):
     _inherit = 'stock.picking'

     x_sj_supplier = fields.Char(string='Nomor Surat Jalan Supplier')
     x_tgl_sj_supp = fields.Datetime(string='Tanggal Surat Jalan Supplier')
     x_tgl_kedatangan_bahan = fields.Datetime(string='Tanggal Terima Bahan')
     is_delivery = fields.Boolean(default=False, track_visibility='onchange')
     x_po_cus = fields.Char(compute='get_po_cus')
     x_group_id_so = fields.Char(compute='get_procurement_group_so')
     x_tkr_guling = fields.Selection([
          ('full', 'Full Delivery'),
          ('partial', 'Partial  Delivery'),
          ('exchange', 'Exchange  Delivery')
     ], string='Delivery Type', default = 'full' , required=True, track_visibility='onchange')
     x_send_to_fac = fields.Selection([('yes', 'Yes'),('no', 'No')],
                                      string='Send to FAC',
                                      default = 'no' , readonly=True, track_visibility='onchange')
     x_status_pengiriman = fields.Selection([
          ('belum_kirim', 'Belum Kirim'),
          ('proses_kirim', 'Proses Pengiriman'),
          ('diterima_cust', 'Diterima Customer'),
          ('sjk_kembali', 'SJK Kembali')
     ], string="Status Pengiriman", default='belum_kirim', readonly=True, track_visibility='onchange')
     x_flag_kirim_barang = fields.Boolean(default=False)
     x_flag_terima_cust = fields.Boolean(default=False)
     x_flag_receipt = fields.Boolean(default=False)
     x_no_sj_internal = fields.Char(string="No SJ Internal", readonly=True)
     x_is_it = fields.Boolean(compute='cek_user_it')
     is_responsible = fields.Boolean()
     x_kebutuhan_pengiriman_ids = fields.Many2many('x.kebutuhan.pengiriman', string="Kebutuhan Pengiriman",
                                                   related='partner_id.x_kebutuhan_pengiriman_ids')
     x_kebutuhan_pengiriman_ids2 = fields.Many2many('x.kebutuhan.pengiriman', string="Kebutuhan Pengiriman",
                                                   related='partner_id.parent_id.x_kebutuhan_pengiriman_ids')

     # uswa-tambah field many2one
     id_ticket_helpdesk = fields.Many2one('helpdesk_lite.ticket', string="Ticket Name")

     # Fungsi button print_sjk
     def print_sjk(self):
          for row in self:
               is_delivery = row.is_delivery
               x_no_sj_internal = row.x_no_sj_internal
               customer_obj = ""
               partner_id_parent = row.partner_id.parent_id
               if partner_id_parent:
                    customer_obj = row.env['res.partner'].search([('id', '=', partner_id_parent.id)])
               else:
                    partner_id = row.partner_id
                    customer_obj = row.env['res.partner'].search([('id', '=', partner_id.id)])

               for o in customer_obj:
                    block_pengiriman = o.x_block_pengiriman

                    if block_pengiriman == 'open':
                         # Jika tidak ada no sj internal
                         if not x_no_sj_internal:
                              sequence = self.env['ir.sequence'].next_by_code('seq.sjinternal') or ('New')
                              row.update({'x_no_sj_internal': sequence})

                         row.write({'is_delivery': True})
                         return row.env['report'].get_action(self, 'lpj_inventory.report_deliveryslip_custom')

                    # Jika block pengiriman
                    else:
                         return row.message_block_pengiriman()

     # Fungsi button print untuk IT user
     def print_sjk_it(self):
          for pick in self:
               x_no_sj_internal = pick.x_no_sj_internal

               # Jika belum ada sj internal
               if not x_no_sj_internal:
                    # Sequence SJ Internal
                    sequence = self.env['ir.sequence'].next_by_code('seq.sjinternal') or ('New')
                    pick.update({'x_no_sj_internal': sequence})

               self.write({'is_delivery': True})
               return self.env['report'].get_action(self, 'lpj_inventory.report_deliveryslip_custom')

     # Pop message block pengiriman
     @api.multi
     def message_block_pengiriman(self):
          return {
               'name': 'Warning',
               'type': 'ir.actions.act_window',
               'view_type': 'form',
               'view_mode': 'form',
               'res_model': 'message.block.pengiriman',
               'target': 'new',
               'context': {
                    'default_name': "Sorry, your product can not be delivered !",
                    'default_name_second': "Please request to accounting for open this customer"
               }
          }

     # Ketika klik tombol validate di WH
     @api.multi
     def do_new_transfer(self):
          for pick in self:
               # Update tanggal kedatangan bahan hari ini ketika klik tombol validate
               pick.update({'x_tgl_kedatangan_bahan': datetime.now()})

               if pick.state == 'done':
                    raise UserError(_('The pick is already validated'))

               pack_operations_delete = self.env['stock.pack.operation']
               if not pick.move_lines and not pick.pack_operation_ids:
                    raise UserError(_('Please create some Initial Demand or Mark as Todo and create some Operations. '))
               # In draft or with no pack operations edited yet, ask if we can just do everything
               if pick.state == 'draft' or all([x.qty_done == 0.0 for x in pick.pack_operation_ids]):
                    # If no lots when needed, raise error
                    picking_type = pick.picking_type_id
                    if (picking_type.use_create_lots or picking_type.use_existing_lots):
                         for pack in pick.pack_operation_ids:
                              if pack.product_id and pack.product_id.tracking != 'none':
                                   raise UserError(_(
                                        'Some products require lots/serial numbers, so you need to specify those first!'))
                    view = self.env.ref('stock.view_immediate_transfer')
                    wiz = self.env['stock.immediate.transfer'].create({'pick_id': pick.id})
                    # TDE FIXME: a return in a loop, what a good idea. Really.
                    return {
                         'name': _('Immediate Transfer?'),
                         'type': 'ir.actions.act_window',
                         'view_type': 'form',
                         'view_mode': 'form',
                         'res_model': 'stock.immediate.transfer',
                         'views': [(view.id, 'form')],
                         'view_id': view.id,
                         'target': 'new',
                         'res_id': wiz.id,
                         'context': self.env.context,
                    }

               # Check backorder should check for other barcodes
               if pick.check_backorder():
                    view = self.env.ref('stock.view_backorder_confirmation')
                    wiz = self.env['stock.backorder.confirmation'].create({'pick_id': pick.id})
                    # TDE FIXME: same reamrk as above actually
                    return {
                         'name': _('Create Backorder?'),
                         'type': 'ir.actions.act_window',
                         'view_type': 'form',
                         'view_mode': 'form',
                         'res_model': 'stock.backorder.confirmation',
                         'views': [(view.id, 'form')],
                         'view_id': view.id,
                         'target': 'new',
                         'res_id': wiz.id,
                         'context': self.env.context,
                    }
               for operation in pick.pack_operation_ids:
                    if operation.qty_done < 0:
                         raise UserError(_('No negative quantities allowed'))
                    if operation.qty_done > 0:
                         operation.write({'product_qty': operation.qty_done})
                    else:
                         pack_operations_delete |= operation
               if pack_operations_delete:
                    pack_operations_delete.unlink()
          self.do_transfer()
          return

     # BUTTON VALIDATE
     # Hanya Untuk Delivery Order
     @api.multi
     def do_new_transfer_custom(self):
          for pick in self:
               # Custom koding
               pick.update({'x_status_pengiriman': 'sjk_kembali'})

               if pick.state == 'done':
                    raise UserError(_('The pick is already validated'))
               pack_operations_delete = self.env['stock.pack.operation']
               if not pick.move_lines and not pick.pack_operation_ids:
                    raise UserError(_('Please create some Initial Demand or Mark as Todo and create some Operations. '))
               # In draft or with no pack operations edited yet, ask if we can just do everything
               if pick.state == 'draft' or all([x.qty_done == 0.0 for x in pick.pack_operation_ids]):
                    # If no lots when needed, raise error
                    picking_type = pick.picking_type_id
                    if (picking_type.use_create_lots or picking_type.use_existing_lots):
                         for pack in pick.pack_operation_ids:
                              if pack.product_id and pack.product_id.tracking != 'none':
                                   raise UserError(_(
                                        'Some products require lots/serial numbers, so you need to specify those first!'))
                    view = self.env.ref('stock.view_immediate_transfer')
                    wiz = self.env['stock.immediate.transfer'].create({'pick_id': pick.id})
                    # TDE FIXME: a return in a loop, what a good idea. Really.
                    return {
                         'name': _('Immediate Transfer?'),
                         'type': 'ir.actions.act_window',
                         'view_type': 'form',
                         'view_mode': 'form',
                         'res_model': 'stock.immediate.transfer',
                         'views': [(view.id, 'form')],
                         'view_id': view.id,
                         'target': 'new',
                         'res_id': wiz.id,
                         'context': self.env.context,
                    }

               # Check backorder should check for other barcodes
               if pick.check_backorder():
                    view = self.env.ref('stock.view_backorder_confirmation')
                    wiz = self.env['stock.backorder.confirmation'].create({'pick_id': pick.id})
                    # TDE FIXME: same reamrk as above actually
                    return {
                         'name': _('Create Backorder?'),
                         'type': 'ir.actions.act_window',
                         'view_type': 'form',
                         'view_mode': 'form',
                         'res_model': 'stock.backorder.confirmation',
                         'views': [(view.id, 'form')],
                         'view_id': view.id,
                         'target': 'new',
                         'res_id': wiz.id,
                         'context': self.env.context,
                    }
               for operation in pick.pack_operation_ids:
                    if operation.qty_done < 0:
                         raise UserError(_('No negative quantities allowed'))
                    if operation.qty_done > 0:
                         operation.write({'product_qty': operation.qty_done})
                    else:
                         pack_operations_delete |= operation
               if pack_operations_delete:
                    pack_operations_delete.unlink()
          self.do_transfer()
          return

     # Get No PO Customer dari sales order
     @api.one
     def get_po_cus(self):
          origin = self.origin
          if self.group_id:
               for procurement_group in self.group_id:
                    name_reference = procurement_group.name

                    sale_order = self.env['sale.order'].search(['|', ('name', '=', name_reference),('name', '=', origin)])
                    if sale_order:
                         for o in sale_order:
                              no_po_cus = o.x_po_cust
                              self.x_po_cus = no_po_cus
          else:
               sale_order = self.env['sale.order'].search([('name', '=', origin)])
               if sale_order:
                    for o in sale_order:
                         no_po_cus = o.x_po_cust
                         self.x_po_cus = no_po_cus

     # Get Procurement group id di SJK
     @api.one
     def get_procurement_group_so(self):
          if self.group_id:
               # Looping group id
               for o in self.group_id:
                    name = o.name
                    # Masukkan ke dalam variable baru
                    self.x_group_id_so = name


     # Button untuk action_kirim_barang
     @api.multi
     def action_kirim_barang(self):
          for picking in self:
               return picking.update({'x_flag_kirim_barang': True,
                                      'x_status_pengiriman': 'proses_kirim'})

     # Button untuk action terima customer
     @api.multi
     def action_terima_cust(self):
          for picking in self:
               return picking.update({'x_flag_terima_cust': True,
                                      'x_status_pengiriman': 'diterima_cust'})

     # Button insert material internal TF
     @api.multi
     def insert_material(self):
          terms = []
          origin = self.origin
          location_id = self.location_id
          location_dest_id = self.location_dest_id
          state = self.state

          mrp_production_obj = self.env['mrp.production'].search([('name', '=', origin)])
          if mrp_production_obj:
               for row in mrp_production_obj.move_raw_ids:
                    values = {}
                    product_material = row.product_id
                    product_to_consume = row.product_uom_qty
                    product_uom = row.product_uom

                    if product_material.active != False and state in ('draft', 'confirmed'):
                         # Delete line
                         self.delete_move_line()
                         values['name'] = product_material.name
                         values['product_id'] = product_material
                         values['product_uom_qty'] = product_to_consume
                         values['product_uom'] = product_uom
                         values['location_id'] = location_id
                         values['location_dest_id'] = location_dest_id

                         terms.append((0, 0, values))

                    else:
                         raise UserError(_(
                              'You Cannot Insert Material at State '+ self.state +', or Please Check your Status Materials'))

          return self.update({'move_lines': terms})

     # Delete line function
     @api.multi
     def delete_move_line(self):
          move_line_ids = []
          picking_id = self.id

          stock_picking = self.env['stock.picking'].search([('id', '=', picking_id)])
          if stock_picking:
               move_line_ids.append(([5]))

               return self.update({'move_lines': move_line_ids})

     # Cek user IT
     @api.one
     def cek_user_it(self):
          res_user = self.env['res.users'].search([('id', '=', self._uid)])
          if res_user.has_group('base.group_system') or \
                  res_user.has_group('account.group_account_manager'):
               self.x_is_it = True
          else:
               self.x_is_it = False

     # Fungsi agar is_delivery False ketika create backorder
     def copy(self, default=None):
          default = dict(default or {})
          default.update({
               'is_delivery': False,
               'x_flag_kirim_barang': False,
               'x_flag_terima_cust': False,
               'x_flag_receipt': False,
               'x_send_to_fac': 'no',
               'x_tkr_guling': 'full',
               'x_status_pengiriman': 'belum_kirim'
          })

          return super(lot_barang, self).copy(default)


class stock_line(models.Model):
     _inherit = 'stock.pack.operation'

     keterangan = fields.Text(string="Keterangan")
     x_total_berat_stc = fields.Float(string="Berat Stc (Kg)", compute='_onchange_packlots_berat', store=True)

     # Untuk perhitungan
     # jumlah berat sticker pada pack_lot_ids
     @api.depends('pack_lot_ids.x_berat_per_lot')
     def _onchange_packlots_berat(self):
          for data in self:
               total = 0
               for row in data.pack_lot_ids:
                   total += row.x_berat_per_lot
               data.x_total_berat_stc = total


     # uswa-tambah fungsi button (name = todo_to_done) buat move qty dati field 'To Do' ke 'Done'
     @api.multi
     def todo_to_done(self):
          self.ensure_one()
          self.name = "New name"

          for row in self:
               a_list_lot = row.pack_lot_ids

               if a_list_lot:
                    for lot in a_list_lot:
                         lot.qty = lot.qty_todo
                         # lot.qty_todo = 0

          return {
               "type": "ir.actions.do_nothing",
          }


     # uswa- tambah fungsi button (name = print_popup) buat print data di popup lot
     def print_popup(self):
          # self.write({'is_delivery': True})
          return self.env['report'].get_action(self, 'lpj_inventory.report_delivery_lot_popup')





class sstock_inventory_lot(models.Model):
     _inherit = 'stock.inventory.line'

     x_kode_customer = fields.Char(string = 'Kode Customer')
     @api.multi
     def stock_inventorylot(self):
          return {
               'name': 'Go to website',
               'res_model': 'ir.actions.act_url',
               'type': 'ir.actions.act_url',
               'url': 'http://192.168.1.8:8086/lot/production/lot_adjust?id=4&jumlah=1' + '&name=' + str(
                    self.prod_lot_id.name) + '&bahan=' + '&awal=False' + '&akhir=False' + '&print=1' + '&cus=' + str(self.x_kode_customer) + '&date=' + '&categ= STC' + '&qtyakhir='

               # 'url': 'http://192.168.1.8:8086/lot/production/lot_adjust?id=3&jumlah=' + '&name=' + str(
               #      self.name) + '&bahan=' + '&awal=False' + '&akhir=False' + '&print=' + str(
               #      self.x_jml_print) + '&cus=' + '&date=' + '&categ=' + '&qtyakhir=' + str(
               #      self.x_qty_akhir)
          }

class stock_scrap(models.Model):
     _inherit = 'stock.scrap'

     keterangan = fields.Text(string="Keterangan")
