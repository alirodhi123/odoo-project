# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp

class property_bom_line(models.Model):
    _inherit = 'mrp.bom.line'
    _name = 'mrp.bom.line'

    product_qty = fields.Float(store=True, string="Product Quantity", require=True, Copy=True,
                               digits=dp.get_precision('Payment Terms'))

