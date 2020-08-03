from odoo import models, fields, api, _


class inventory_adjustment(models.Model):
    _inherit = 'stock.inventory'

    x_tipe_adj = fields.Many2one('x.tipe.adjustment', string="Adjustment Type")
    create_uid = fields.Many2one('res.users', readonly=True, default=lambda self: self.env.uid,)


class tipe_adjustment(models.Model):
    _name = 'x.tipe.adjustment'

    name = fields.Char(string="Adjustment Type")