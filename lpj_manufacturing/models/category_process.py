
from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta


class CategoryProcess(models.Model):
    _name = 'x.category.process'

    name = fields.Char(string="Nama Proses")