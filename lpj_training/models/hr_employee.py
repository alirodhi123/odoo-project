from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    training_count = fields.Integer(compute='_compute_training_count', string="Training")
    trainer_count = fields.Integer(string="Trainer")

    @api.multi
    def _compute_training_count(self):
        for o in self:
            var_schedule_line = self.env['x.training.schedule.line'].search([('x_name_employee', '=', o.id)])
            if var_schedule_line:
                for row in var_schedule_line:
                    state = row.training_schedule_id.state

                    if state == 'done':
                        log_training_data = var_schedule_line.sudo().read_group([('x_name_employee', 'in', self.ids)], ['x_name_employee'],
                                                                                  ['x_name_employee'])
                        result = dict((data['x_name_employee'][0], data['x_name_employee_count']) for data in log_training_data)
                        for employee in self:
                            employee.training_count = result.get(employee.id, 0)
