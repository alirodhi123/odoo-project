# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import amount_to_text_en, datetime, timedelta
from odoo.tools import amount_to_text
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class inline_project(models.Model):
    _name = 'project.task.line'

    x_project_task_id = fields.Many2one('project.task')
    x_users = fields.Many2one('res.users','PIC')
    x_task = fields.Text('Action')
    x_date_task = fields.Date(string='Due Date')
    x_date_finish = fields.Date(string='Finish Date')
    x_attch_file = fields.Binary(string='Attachment')
    x_category_problem = fields.Selection([('man','Man'),('machine','Machine'),('method','Method'),('material','Material'),('environmental','Environmental')],string='Category')
    x_akar_masalah = fields.Text('Akar Masalah')
    x_status = fields.Selection([('draft', 'Draft'), ('inprogress', 'In Progress'), ('done', 'Done')],default='draft' ,string='Status')
    # x_due_date = fields.datetime('Duedate')

class inherit_project_task(models.Model):
    _inherit = 'project.task'

    x_project_task_line = fields.One2many('project.task.line','x_project_task_id','Task')
    x_name = fields.Char(string="No Laporan", readonly=True)
    x_duration = fields.Selection([('1','1'),('2','2'),('3','3'),('5','5'),('8','8'),('13','13'),
                                   ('21','21'),('34','34'),('55','55'),('89','89')],string='Duration (H)')
    # x_category_status = fields.Selection([('minor', 'Minor'), ('major', 'Major')] ,string='Status Project')
    x_sprint = fields.Many2one('x.sprint.project',string='Sprint')
    x_department = fields.Many2one('hr.department',string='Department')

    x_role = fields.Many2one('x.project.roles', string='User Role')
    x_requirement = fields.Text(string='Requirements')
    x_reason = fields.Text(string='Reason')
    #
    x_acceptance_criteria = fields.Text(string='Acceptance Criteria')
    x_edge_criteria = fields.Text(string='Edge Criteria')

    x_category_problems = fields.Many2one('x.project.problem.category', string='Category Problems')
    x_description_problems = fields.Text( string='Problem Description')



    @api.onchange('x_duration')
    def onchange_x_duration(self):
        self.planned_hours = self.x_duration

    x_priority = fields.Many2one('x.project.priority',string='Priority')

    # Sequences
    @api.model
    def create(self, vals):
        vals['x_name'] = self.env['ir.sequence'].next_by_code('seq.cca') or ('New')

        result = super(inherit_project_task, self).create(vals)
        return result

class priority_project(models.Model):
    _name = 'x.project.priority'

    name = fields.Integer(string='Priority')
    # priority_task_id = fields.Many2one('project.task')

class sprint_project(models.Model):
    _name = 'x.sprint.project'

    name = fields.Char('Sprint')
    x_periode_start = fields.Date('Date Start')
    x_periode_end = fields.Date('Date End')

    @api.onchange('x_periode_start')
    def calculation_sprint(self):
	date_format = '%Y-%m-%d'
        start_date = datetime.strptime(str(self.x_periode_start), date_format)
        self.x_periode_end = start_date + relativedelta(days=int(14))
class sprint_project_role(models.Model):
    _name = 'x.project.roles'

    name = fields.Char(string='Roles')

class problems_category(models.Model):
    _name = 'x.project.problem.category'

    name = fields.Char(string='Problem Category')

