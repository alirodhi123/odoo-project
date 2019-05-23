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
     is_delivery = fields.Boolean(default=False)
     x_po_cus = fields.Char(compute='get_po_cus')
     x_group_id_so = fields.Char(compute='get_procurement_group_so')


     # Button print SJK
     @api.multi
     def print_sjk(self):
          self.write({'is_delivery': True})
          return self.env['report'].get_action(self, 'lpj_inventory.report_deliveryslip')

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


class stock_line(models.Model):
     _inherit = 'stock.pack.operation'

     keterangan = fields.Text(string="Keterangan")

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




