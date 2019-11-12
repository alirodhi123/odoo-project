from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError


class TrainingTags(models.Model):
    _name = 'training.tags'
    _description = "Tags of category in training"

    name = fields.Char(required=True)
    color = fields.Integer(string='Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]