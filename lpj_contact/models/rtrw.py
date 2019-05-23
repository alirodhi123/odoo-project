# -*- coding: utf-8 -*-
# import subprocess

from odoo import models, fields, api
# import odoo.addons.decimal_precision as dp


class inherit_contact_partner(models.Model):

     _inherit = 'res.partner'

     x_rt = fields.Char(string = 'RT')
     x_rw = fields.Char(string='RW')
     x_npwp = fields.Char(string = 'NPWP')
     x_pkp = fields.Boolean(string = 'PKP')
     x_kode_customer = fields.Char(string='Kode Customer')

     x_customer_service = fields.Many2one('res.users',string = 'Customer Services')




class termin_line(models.Model):
     _name = 'x.termin'

     name = fields.Char(string = 'Nama Termin')
     Description = fields.Text(string = 'Description')