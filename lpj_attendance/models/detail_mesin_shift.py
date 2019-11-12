from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class shift_mesin(models.Model):
    _name = 'x.shift.mesin'

    name = fields.Char(string="Kode Mesin")
    x_tipe_mesin_shift = fields.Char(string="Tipe Mesin")
    x_tipe_proses_mesin_shift = fields.Char(string="Tipe Proses Mesin")