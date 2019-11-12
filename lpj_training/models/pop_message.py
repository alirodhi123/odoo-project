from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError


class PopMessage(models.Model):
    _name = 'x.pop.message'

    name = fields.Char(string="Message")
    training_schedule_id = fields.Many2one('x.training.schedule', string="Training Schedule")
