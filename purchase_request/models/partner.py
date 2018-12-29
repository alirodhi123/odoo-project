from odoo import api, fields, models, _

class partner(models.Model):
    _inherit = "res.partner"

    termin_vendor = fields.Many2one('account.payment.term', company_dependent=True)