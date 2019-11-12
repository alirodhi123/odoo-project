from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError


class HR_Employee(models.Model):
    _inherit = 'hr.employee'

    x_employee_training_ids = fields.One2many('x.employee.training', 'x_employee_id')