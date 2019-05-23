from odoo import api, models, fields


class BufferTags(models.Model):
    _name = 'buffer.tags'
    _description = "Tags of label in manufacturing order"

    name = fields.Char(required=True)
    color = fields.Integer(string='Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]