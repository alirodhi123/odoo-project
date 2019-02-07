
from odoo import models, fields, api, _

class res_partner(models.Model):
    _inherit = 'res.partner'

    account_number_bank = fields.Char(compute='get_partner_bank')
    bank_id = fields.Char(compute='get_partner_bank')
    street_bank = fields.Char(compute='get_partner_bank')

    @api.one
    def get_partner_bank(self):
        vendor = self.name
        partner_bank = self.env['res.partner.bank'].search([('partner_id', '=', vendor)])
        if partner_bank:
            self.account_number_bank = partner_bank.acc_number
            for row in partner_bank.bank_id:
                bank_name = row.name
                street = row.street

                self.street_bank = street
                self.bank_id = bank_name

