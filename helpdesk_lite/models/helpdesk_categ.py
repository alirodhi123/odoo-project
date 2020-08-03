
from odoo import api, fields, models


class categ_ticket(models.Model):
    _name = 'categ.ticket'

    name = fields.Char(string="Nama Kategori")