# -*- coding: utf-8 -*-
import subprocess

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp



class lot_sj(models.Model):
     _inherit = 'stock.pack.operation'
     # x_qty_satuan = fields.Integer(string='Quantity Satuan')
     # x_lot_sj = fields.Char(string='Jumlah Lot', readonly=False)
     # x_jml_print = fields.Integer(string='Jumlah Print', readonly=False)
     # x_customer = fields.Many2one('res.partner', related='picking_id.partner_id', string='customer', readonly=False)
     # x_customer_code = fields.Char(string='kode cust', readonly=False, related='x_customer.x_kode_customer')
     # x_categ_id = fields.Many2one(readonly=True, related='product_id.product_tmpl_id.categ_id')

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


class master_lot(models.Model):
     _inherit = 'stock.production.lot'

     x_jml_print = fields.Integer(string='Jumlah Print: ')
     x_qty_akhir = fields.Integer(string = 'Quantity akhir bahan: ')

     @api.multi
     def action_master(self):
          return {
               'name': 'Go to website',
               'res_model': 'ir.actions.act_url',
               'type': 'ir.actions.act_url',
               'url': 'http://192.168.1.8:8086/Lot?id=3&jumlah=' + '&name=' + str(self.name) + '&bahan='+ str(self.product_id.name)+ '&awal=False' + '&akhir=False' + '&print=' + str(self.x_jml_print) + '&cus='+ '&date=' + '&categ=' + '&qtyakhir=' + str(self.x_qty_akhir)
          }


