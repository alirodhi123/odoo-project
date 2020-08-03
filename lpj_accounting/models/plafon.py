
from odoo import models, fields, api, _

class Plafon(models.Model):
    _name = 'x.plafon'

    @api.model
    def _get_default_user(self):
        return self.env['res.users'].browse(self.env.uid)

    x_partner_id = fields.Many2one('res.partner')
    x_amount_plfn = fields.Monetary(string='Amount')
    currency_id = fields.Many2one('res.currency')
    x_name_plfn = fields.Char(string="Name")
    x_status_plfn = fields.Char(string='Status')
    x_date_plfn = fields.Date(string='Date')
    x_user_input_plfn = fields.Many2one('res.users', string="User Input",
                                        default=_get_default_user, readonly=True)