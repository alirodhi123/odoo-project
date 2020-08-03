from odoo import api, fields, models, tools, SUPERUSER_ID, _
import re
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import AccessError


class category_problem(models.Model):
    _name = 'categ.problem'

    name = fields.Char(string="Detail Problem")