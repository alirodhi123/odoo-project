from odoo import models, fields, api, _


class res_partner(models.Model):
    _inherit = 'res.partner'

    x_available_foot = fields.Monetary(compute='_compute_amount', string="Available Amount")
    x_plafon_line = fields.One2many('x.plafon', 'x_partner_id', string="Transaction History")

    @api.one
    @api.depends('x_plafon_line.x_amount_plfn')
    def _compute_amount(self):
        amount = 0
        for row in self.x_plafon_line:
            amount += row.x_amount_plfn

        self.x_available_foot = amount