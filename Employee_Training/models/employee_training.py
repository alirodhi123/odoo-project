from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError


class TrainingTraining(models.Model):
    _inherit = 'training.training'

    x_employee_training_ids = fields.One2many('x.employee.training', 'x_training_id')
    x_training_name = fields.Char(string="Training Name")
    x_department = fields.Many2one('hr.department', string="Department", related='employee_id.department_id', readonly=True)
    # x_category_training = fields.Many2many('training.tags', string="Category Training", required=True)
    x_category_training = fields.Selection([('internal', 'Training Internal'), ('eksternal', 'Training Eksternal')], string="Category Training", required=True)


    # Main Function button insert details employee
    @api.multi
    def function_details_employee(self):
        for training in self:
            training.delete_employee_details()
            training.get_details_employee()

    # Function insert employee
    @api.multi
    def get_details_employee(self):
        department_id = self.x_department
        temp = []

        employee = self.env['hr.employee']
        department = self.env['hr.department'].search([('id', '=', department_id.id)])
        if department:
            employee_ids = employee.search([('department_id', '=', department_id.id)])
            for row in employee_ids:
                var = row.name_related
                emp_department_id = row.department_id
                emp_id = row.id
                emp_work_email = row.work_email
                emp_job_title = row.job_id
                emp_manager = row.parent_id


                values = {}
                values['x_name_employee'] = emp_id
                values['x_work_email'] = emp_work_email
                values['x_department'] = emp_department_id
                values['x_job_tittle'] = emp_job_title
                values['x_manager'] = emp_manager
                temp.append((0, 0, values))

            return self.update({'x_employee_training_ids': temp})

    # Function delete employee details
    @api.multi
    def delete_employee_details(self):
        training_id = self.id
        temp = []

        x_employee_training = self.env['x.employee.training'].search([('x_training_id', '=', training_id)])
        if x_employee_training:
            temp.append(([5]))

            return self.update({'x_employee_training_ids': temp})


    @api.multi
    def create_training(self):
        for training in self:
            ac = training.env['ir.model.data'].xmlid_to_res_id('Employee_Training.course_schedule_form_view', raise_if_not_found=True)
            employee_details = len(training.x_employee_training_ids)
            if employee_details != 0:
                result = {
                    'name': '2nd class',
                    'view_type': 'form',
                    'res_model': 'course.schedule',
                    'view_id': ac,
                    'context': {

                    },
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form'
                }
                return result



class EmployeeTraning(models.Model):
    _name = 'x.employee.training'

    x_training_id = fields.Many2one('training.training')
    x_name_employee = fields.Many2one('hr.employee', string="Name")
    x_work_email = fields.Char(string="Work Email")
    x_department = fields.Many2one('hr.department', string="Department")
    x_job_tittle = fields.Many2one('hr.job', string="Job Title")
    x_manager = fields.Many2one('hr.employee', string="Manager")
