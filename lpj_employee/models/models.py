# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Employee(models.Model):
    _inherit = 'hr.employee'

    x_alamat = fields.Text(string="Address")
    x_join_date = fields.Date(string="Join Date")
    x_resign_date = fields.Date(string="Resign Date")

