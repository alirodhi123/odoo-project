# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp

class x_pertanyaan (models.Model):
     _name = 'x.pertanyaan.tinta'

     name = fields.Char(string = 'nama')
