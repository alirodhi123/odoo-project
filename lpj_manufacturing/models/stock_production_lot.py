from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Production_lots(models.Model):
    _inherit = 'stock.move.lots'

    # LOT REFERENCE
    x_lot_reference = fields.Char(string="Lot Reference", readonly=True)
    x_product_id = fields.Char(string="Product")


class Lot_Work_Order(models.Model):
    _name = 'x.move.lots'

    workorder_id = fields.Many2one('mrp.workorder')
    x_lot = fields.Char(string="Lot")
    x_product_id = fields.Many2one('product.product', string="Product")
    x_to_consume = fields.Char(string="To Consume")



