
from odoo import models, fields, api, _

class res_partner(models.Model):
    _inherit = 'res.partner'

    account_number_bank = fields.Char()
    bank_id = fields.Char()
    street_bank = fields.Char()
    trust_custom = fields.Selection([('good', 'Good Debtor'), ('normal', 'Normal Debtor'), ('bad', 'Bad Debtor'), ('block', 'Block Debtor')],
                             string='Degree of trust you have in this debtor', default='block')

    # @api.multi
    # def get_partner_bank(self):
    #     vendor = self.name
    #     partner_bank = self.env['res.partner.bank'].search([('partner_id', '=', vendor)])
    #     if partner_bank:
    #         self.account_number_bank = partner_bank.acc_number
    #         for row in partner_bank.bank_id:
    #             bank_name = row.name
    #             street = row.street
    #
    #             self.street_bank = street
    #             self.bank_id = bank_name

