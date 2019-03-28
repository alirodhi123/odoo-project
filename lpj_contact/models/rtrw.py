# -*- coding: utf-8 -*-
# import subprocess

from odoo import models, fields, api
# import odoo.addons.decimal_precision as dp


class inherit_contact_partner(models.Model):
     _name = 'res.partner'
     _inherit = 'res.partner'

     x_rt = fields.Char(string = 'RT')
     x_rw = fields.Char(string='RW')
     x_npwp = fields.Char(string = 'NPWP')
     x_pkp = fields.Boolean(string = 'PKP')
     x_kode_customer = fields.Char(string='Kode Customer')
     trust = fields.Selection(
                    [('good', 'Good Debtor'), ('normal', 'Normal Debtor'), ('bad', 'Bad Debtor'), ('block', 'Block Debtor')],
                    string='Degree of trust you have in this debtor', default='block')

     # trust_custom = fields.Selection(
     #      [('good', 'Good Debtor'), ('normal', 'Normal Debtor'), ('bad', 'Bad Debtor'), ('block', 'Block Debtor')],
     #      string='Degree of trust you have in this debtor', default='block')

     # x_termin_id = fields.Many2one('x.termin', string='Berdasarkan')
     # x_payment_type = fields.Selection([('dp','DP'),('nondp','NON DP')], string = 'Payment Type')
     # x_lama_termin = fields.Integer(string = 'Lama Termin')

class termin_line(models.Model):
     _name = 'x.termin'

     name = fields.Char(string = 'Nama Termin')
     Description = fields.Text(string = 'Description')