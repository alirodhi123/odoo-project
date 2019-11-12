
from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError


class NewTraining(models.Model):
    _name = 'x.training.training'
    _inherit = 'mail.thread'
    _description = 'Training'


    def _default_employee(self):
        return self.env.context.get('default_employee_id') or self.env['hr.employee'].search(
            [('user_id', '=', self.env.uid)], limit=1)

    name = fields.Char()
    employee_id = fields.Many2one('hr.employee', string='Employee', index=True, readonly=True,
                                  states={'new': [('readonly', False)], 'hod': [('readonly', False)]},
                                  default=_default_employee, track_visibility="onchange")
    state = fields.Selection(selection=[('new', 'New'),
                                        ('hrd', 'HRD Approve'),
                                        ('reject', 'Reject')],
                             default='new',track_visibility="onchange")
    user_id = fields.Many2one('res.users', string='User', related='employee_id.user_id', related_sudo=True,
                              default=lambda self: self.env.uid, readonly=True, track_visibility="onchange")
    line_count = fields.Integer(string='Purchase Request Line count', compute='_compute_line_count', readonly=True, track_visibility="onchange")
    x_employee_training_ids = fields.One2many('x.employee.training', 'x_training_id', track_visibility="onchange")
    x_training_name = fields.Char(string="Training Name", track_visibility="onchange")
    x_department = fields.Many2one('hr.department', string="Department", related='employee_id.department_id',
                                   readonly=True, track_visibility="onchange")
    x_category_training = fields.Selection([('internal', 'Training Internal'), ('eksternal', 'Training Eksternal')],
                                           string="Category Training", required=True, track_visibility="onchange")
    x_department = fields.Many2one('hr.department', string="Department", related='employee_id.department_id',
                                   readonly=True, track_visibility="onchange")
    x_origin = fields.Many2one('x.training.schedule', string="Training Schedule", track_visibility="onchange")

    @api.model
    def create(self, vals):
        res = super(NewTraining, self).create(vals)

        # Sequence
        sequence = self.env['ir.sequence'].next_by_code('sequence.x.training') or ('New')
        res.update({'name': sequence})

        return res

    @api.depends('x_employee_training_ids')
    def _compute_line_count(self):
        self.line_count = len(self.mapped('x_employee_training_ids'))


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


    # Function Create Training Schedule
    @api.multi
    def create_training(self):
        for training in self:
            schedule_obj = self.env['x.training.schedule']
            employee_details = len(training.x_employee_training_ids)
            source_document = training.x_origin
            category_training = training.x_category_training
            employee_id = training.employee_id
            datas = []

            # Jika training schedule belum ada
            if not source_document:
                if employee_details != 0:
                    for row in training.x_employee_training_ids:
                        employee_name = row.x_name_employee.id
                        email_emp = row.x_work_email
                        department_emp = row.x_department.id
                        job_tittle_emp = row.x_job_tittle.id
                        manager_emp = row.x_manager.id

                        values = {}
                        values['x_name_employee'] = employee_name
                        values['x_work_email'] = email_emp
                        values['x_department'] = department_emp
                        values['x_job_tittle'] = job_tittle_emp
                        values['x_manager'] = manager_emp
                        datas.append((0, 0, values))

                    # Create Training Schedule
                    schedule_obj.create({
                        'training_id': training.id,
                        'capacity': training.line_count,
                        'x_category_training_schedule': category_training,
                        'x_employee_id': employee_id.id,
                        'training_schedule_ids': datas,
                    })

                    # Cek apakah training schedule sudah ada,
                    # jika belum ada maka create training schedule dan
                    # update source document dengan training schedule id
                    schedule_obj_cek = self.env['x.training.schedule'].search([('training_id', '=', self.id)])
                    if schedule_obj_cek:
                        for o in schedule_obj_cek:
                            training.update({'x_origin': o.id})

                        # Message
                        result = {
                            'name': 'Success',
                            'view_type': 'form',
                            'res_model': 'x.pop.message',
                            'target': 'new',
                            'context': {
                                'default_name': "Your Training Schedule Has Been Created!",
                                'default_training_schedule_id': training.x_origin.id
                            },
                            'type': 'ir.actions.act_window',
                            'view_mode': 'form'
                        }
                        return result

            # Jika training schedule sudah ada
            else:
                # Message
                result = {
                    'name': 'Message',
                    'view_type': 'form',
                    'res_model': 'x.pop.message',
                    'target': 'new',
                    'context': {
                        'default_name': "Your Training Schedule Already Exist!",
                        'default_training_schedule_id': training.x_origin.id
                    },
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form'
                }
                return result


    @api.multi
    def action_new(self):
        self.state = 'new'

    @api.multi
    def action_hrd(self):
        self.state = 'hrd'

    @api.multi
    def action_reject(self):
        self.state = 'reject'


class EmployeeTraning(models.Model):
    _name = 'x.employee.training'

    x_training_id = fields.Many2one('x.training.training')
    x_name_employee = fields.Many2one('hr.employee', string="Name")
    x_work_email = fields.Char(string="Work Email")
    x_department = fields.Many2one('hr.department', string="Department")
    x_job_tittle = fields.Many2one('hr.job', string="Job Title")
    x_manager = fields.Many2one('hr.employee', string="Manager")



