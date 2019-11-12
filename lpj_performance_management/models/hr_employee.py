from odoo import models, fields, api


class HREmployee(models.Model):
    _inherit = 'hr.employee'

    se_count_employee = fields.Integer(compute='_compute_se_count_employee')

    @api.multi
    def _compute_se_count_employee(self):
        for o in self:
            se_data = o.env['x.self.eval'].sudo().read_group([('x_employee_id', 'in', self.ids)],
                                                                   ['x_employee_id'], ['x_employee_id'])
            result = dict((data['x_employee_id'][0], data['x_employee_id_count']) for data in se_data)
            for employee in self:
                employee.se_count_employee = result.get(employee.id, 0)
