# -*- coding: utf-8 -*-
import subprocess

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime, time
import odoo.addons.decimal_precision as dp



class lot_sj(models.Model):
     _inherit = 'stock.pack.operation'
     x_qty_satuan = fields.Integer(string='Quantity Satuan')
     x_lot_sj = fields.Char(string='Jumlah Lot', readonly=False)
     x_jml_print = fields.Integer(string='Jumlah Print', readonly=False)
     x_customer = fields.Many2one('res.partner', related='picking_id.partner_id', string='customer', readonly=False)
     x_customer_code = fields.Char(string='kode cust', readonly=False, related='x_customer.x_kode_customer')
     x_categ_id = fields.Many2one(readonly=True, related='product_id.product_tmpl_id.categ_id')

     # uswa-tambah field untuk nampung format barcode lotnya
     x_format_barcode = fields.Char(string='format barcode')
     x_expdate_barcode =fields.Datetime(string='exp barcode')

     @api.multi
     def action(self):
          return {
               'name': 'Go to website',
               'res_model': 'ir.actions.act_url',
               'type': 'ir.actions.act_url',
               'url': 'http://192.168.1.8:8086/Lot?id=2&jumlah=' + str(self.x_lot_sj) +'&name='+ str(self.picking_id.name)+'&bahan='+ str(self.product_id.display_name)+'&awal=False'+'&akhir=False'+'&print='+ str(self.x_jml_print) +'&cus='+ str(self.x_customer_code)+'&date='+ str(self.picking_id.x_tgl_kedatangan_bahan)+'&categ='+ str(self.x_categ_id.name)+ '&qtyakhir='
          }

     @api.onchange ('product_id')
     def _tgl_terima(self):
          self.x_tgl_terima = self.picking_id.x_tgl_kedatangan_bahan


     # FUNGSI CREATE LOT
     @api.multi
     def create_lot_barcode(self):
          for operation in self:
               jml_lotsj = int(operation.x_lot_sj)
               tgl_dtng = operation.picking_id.x_tgl_kedatangan_bahan
               product = operation.product_id
               lot_obj = operation.env['stock.production.lot']

               if jml_lotsj > 0:
                    temp = self.picking_id.name
                    sjk = temp.split('/', 1)[1]

                    operation.x_format_barcode = sjk

                    # FUNGSI CREATE MASTER LOT
                    increment = 1
                    for i in range(jml_lotsj):
                         lot_obj.create({
                              'name': str(operation.x_format_barcode) + "-" + str(increment),
                              'product_id': product.id
                         })
                         increment += 1

                    # self.picking_id.name
                    # self.product_id.display_name
                    # self.x_jml_print
                    # self.x_customer_code
               if tgl_dtng:
                    # six_months_after = tgl_dtng + relativedelta(months=6)
                    # self.x_expdate_barcode = six_months_after

                    date_format = "%Y-%m-%d %H:%M:%S"
                    six_months_after = datetime.strptime(str(tgl_dtng), date_format) + relativedelta(months=6)
                    operation.x_expdate_barcode = six_months_after

                    # self.x_categ_id.name
               return operation.message_create_lot()
               # return self.env['report'].get_action(self, 'lpj_inventory.report_generate_barcode')

     @api.multi
     def message_create_lot(self):
          return {
               'name': 'Success',
               'type': 'ir.actions.act_window',
               'view_type': 'form',
               'view_mode': 'form',
               'res_model': 'message.create.lot',
               'target': 'new',
               'context': {
                    'default_name': "The master lot has been created",
               }
          }


class master_lot(models.Model):
     _inherit = 'stock.production.lot'

     x_jml_print = fields.Integer(string='Jumlah Print: ')
     x_qty_akhir = fields.Integer(string = 'Quantity akhir bahan: ')
     x_berat_per_lot_lot = fields.Float(string="Berat per Lot (gr)", compute='compute_berat_per_lot', digits=(12,4))
     x_berat_per_pcs_lot = fields.Float(string="Berat per Pcs (gr)", readonly=True, digits=(12,4))

     x_is_admin = fields.Boolean(string="Check Admin", compute='is_admin')

     @api.multi
     def action_master(self):
          return {
               'name': 'Go to website',
               'res_model': 'ir.actions.act_url',
               'type': 'ir.actions.act_url',
               'url': 'http://192.168.1.8:8086/Lot?id=3&jumlah=' + '&name=' + str(self.name) + '&bahan='+ str(self.product_id.name)+ '&awal=False' + '&akhir=False' + '&print=' + str(self.x_jml_print) + '&cus='+ '&date=' + '&categ=' + '&qtyakhir=' + str(self.x_qty_akhir)
          }


     @api.one
     def is_admin(self):
          res_user = self.env['res.users'].search([('id', '=', self._uid)])
          if res_user.has_group('base.group_system'):
               self.x_is_admin = True
          else:
               self.x_is_admin = False

     @api.one
     def compute_berat_per_lot(self):
          berat_per_pcs = self.x_berat_per_pcs_lot
          qty = self.product_qty

          self.x_berat_per_lot_lot = qty * berat_per_pcs


