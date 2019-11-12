from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api


class WorkCenters_msr(models.Model):
    _inherit = 'mrp.workcenter'

    x_speet_per_mnt = fields.Float(string="Speed per Menit (m)")


