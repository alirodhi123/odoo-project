# -*- coding: utf-8 -*-
import subprocess

from odoo import models, fields, api
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




     @api.onchange('x_qty_meter')
     def meter_to_pcs(self):
          self.x_jml_prod = 0
          for x in self.x_layout_product:
               self.x_jml_prod = self.x_jml_prod + x.x_number
               if x.x_type == 'arround':
                    self.x_lebaran_bahan = x.x_jumlah / 1000
               self.qty_producing = int((self.x_qty_meter * self.x_jml_prod) / self.x_lebaran_bahan)

class lot_operation(models.Model):
     _name = 'x.lot.operation'

     x_routing_process = fields.Many2one('mrp.workorder', string='Routing Proses')
     x_user = fields.Many2one('res.partner', string='Operator')
     x_routing = fields.Many2one('mrp.workorder', string='Routing Proses')
     name = fields.Many2one('stock.production.lot', string='Nomor Lot')


class mrp_inherit(models.Model):
    _inherit = 'mrp.workcenter.productivity'

    x_wo_rp = fields.Many2one('mrp.workorder', string='Routing Proses')
    x_wo_user = fields.Many2one('res.partner', string='Operator')
    x_wo_lot = fields.Many2many('stock.production.lot', string='Nomor Lot')


