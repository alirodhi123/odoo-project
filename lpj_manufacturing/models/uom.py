# -*- coding: utf-8 -*-
import subprocess

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp



class sale_custom(models.Model):
     _inherit = 'mrp.production'

     mrp_product_id = fields.Many2one('product.product', readonly=True)
     x_mrp_prd_temp = fields.Many2one('product.template', string='Product Template', related='mrp_product_id.product_tmpl_id')
     x_mrp_uom_area = fields.Float(related="x_mrp_prd_temp.x_tot_area")
     # x_mrp_m_qty = fields.Float(compute='_get_total', string="Quantity (m2)")

     # @api.one
     # def _get_total(self):
     #      self.x_mrp_m_qty = self.x_mrp_uom_area * self.product_qty
