from odoo import api, models, fields


class category_masalah_inspection(models.Model):
    _name = 'problem.tags'
    _description = "Tags of problem's tasks, issues..."

    name = fields.Char(required=True)
    color = fields.Integer(string='Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]


class jenis_mesin_inspection(models.Model):
    _name = 'x.mesin.tags'
    _description = "Tags of machine..."

    name = fields.Char(required=True)
    color = fields.Integer(string="Color Index")

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]
