# -*- coding: utf-8 -*-
import subprocess

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp



class lot_workorder_stock(models.Model):
     _inherit = 'stock.production.lot'

     x_lotworkorder_id = fields.One2many('x.lot.workorder', 'x_production_lot')
     x_tampungan_qty = fields.Integer('Tampungan', compute = '_xtampungan')

     @api.one
     def _xtampungan(self):
          self.x_tampungan_qty = self.product_qty

     @api.onchange('product_qty')
     def _trigger_lot(self):
         selisih = self.x_tampungan_qty - self.product_qty
         for a in self.x_lotworkorder_id:
              if a.x_qty_lot <> 0:
                   a.x_qty_lot = a.x_qty_lot - selisih
                   break
              else:
                   a.x_qty_lot = 0
         self.x_tampungan_qty = self.product_qty



class lot_workorder(models.Model):
     _name = 'x.lot.workorder'

     x_production_lot = fields.Many2one('stock.production.lot', string = 'Lot Header')
     x_internal_lot = fields.Char(string = 'Lot Internal')
     x_supplier_lot = fields.Char(string = 'Lot Supplier')
     x_qty_lot = fields.Integer ('Quantity per Roll')