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
    x_attch_file = fields.Many2many('ir.attachment', string='Attachment', attachment=True)
    x_category_problem = fields.Selection([('man','Man'),('machine','Machine'),('method','Method'),('material','Material'),('environmental','Environmental')],string='Category')
    x_akar_masalah = fields.Text('Akar Masalah')
    x_status = fields.Selection([('draft', 'Draft'), ('inprogress', 'In Progress'), ('done', 'Done')],default='draft' ,string='Status')
    x_note = fields.Text(string="Note")
    # x_due_date = fields.datetime('Duedate')

class inherit_project_task(models.Model):
    _inherit = 'project.task'

    x_project_task_line = fields.One2many('project.task.line','x_project_task_id','Task')
    x_name = fields.Char(string="No Laporan", readonly=True)
    x_duration = fields.Selection([('1','1'),('2','2'),('3','3'),('5','5'),('8','8'),('13','13'),
                                   ('21','21'),('34','34'),('55','55'),('89','89')],string='Duration (H)')
    # x_category_status = fields.Selection([('minor', 'Minor'), ('major', 'Major')] ,string='Status Project')
    x_sprint = fields.Many2one('x.sprint.project',string='Sprint')
    x_department = fields.Many2one('hr.department',string='Department Created', compute='get_create_user_dept')
    x_department_assign = fields.Many2one('hr.department',string='Department Assigned', compute='get_assigned_user_dept')
    x_role = fields.Many2one('x.project.roles', string='User Role')
    x_requirement = fields.Text(string='Requirements')
    x_reason = fields.Text(string='Reason')
    x_acceptance_criteria = fields.Text(string='Acceptance Criteria')
    x_edge_criteria = fields.Text(string='Edge Criteria')
    x_category_problems = fields.Many2one('x.project.problem.category', string='Category Problems')
    x_description_problems = fields.Text( string='Problem Description')
    x_sprint_late = fields.Many2one('x.sprint.project',string='Late of Sprint')
    x_duedate_action_plan = fields.Date(string="Due Date Action Plan")
    x_date_actual_closing_cca = fields.Date(string="Date Actual Closing CCA")
    x_description_tindakan_perbaikan = fields.Html(string='Deskripsi Tindakan Perbaikan')
    x_summary = fields.Html(string='Summary')
    x_master_sumber = fields.Many2one('x.master.sumber', string="Sumber")
    x_problem_category_header = fields.Many2one('x.problem.categ', string="Category Problem")
    x_harapan_perbaikan = fields.Text(string="Harapan dari Perbaikan")

    # Analisa Akar masalah
    x_analisa_masalah_ids = fields.One2many('x.analisa.akar.masalah', 'project_task_id')

    # Modul Development
    x_modul_dev_ids = fields.One2many('x.modul.development', 'project_task_id')


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

    # Get Dept ID
    @api.one
    def get_create_user_dept(self):
        for row in self:
            user_create = row.create_uid.id

            row.env.cr.execute("select hd.id from hr_employee he "
                               "join hr_department hd on hd.id = he.department_id "
                               "join resource_resource rr on rr.id = he.resource_id "
                               "join res_users ru on ru.id = rr.user_id "
                               "join res_partner rp on ru.partner_id = rp.id "
                               "where ru.id = '" + str(user_create) + "'")

            sql = self.env.cr.fetchall()
            if sql:
                for o in sql:
                    dept_id = o[0]
                    row.x_department = dept_id

    # Get Dept ID
    @api.one
    def get_assigned_user_dept(self):
        for row in self:
            user_assigned = row.user_id.id

            row.env.cr.execute("select hd.id from hr_employee he "
                               "join hr_department hd on hd.id = he.department_id "
                               "join resource_resource rr on rr.id = he.resource_id "
                               "join res_users ru on ru.id = rr.user_id "
                               "join res_partner rp on ru.partner_id = rp.id "
                               "where ru.id = '" + str(user_assigned) + "'")

            sql = self.env.cr.fetchall()
            if sql:
                for o in sql:
                    dept_id = o[0]
                    row.x_department_assign = dept_id

    # Fungsi auto email
    @api.multi
    def send_mail_cca(self):
        template = self.env.ref('lpj_project.template_mail_cca')
        mail = self.env['mail.template'].browse(template.id)
        mail.send_mail(self.id, force_send=True)  # langsung kirim email

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


class analisa_akar_masalah(models.Model):
    _name = 'x.analisa.akar.masalah'

    project_task_id = fields.Many2one('project.task')
    name = fields.Selection([('why_1', 'Why 1'), ('why_2', 'Why 2'), ('why_3', 'Why 3'),
                             ('why_4', 'Why 4'), ('why_5', 'Why 5')], string="Name")
    x_question = fields.Many2one('x.master.question', string='Question')
    x_answer = fields.Text(string="Answer")


class modul_development(models.Model):
    _name = 'x.modul.development'

    project_task_id = fields.Many2one('project.task')
    modul_dev_name = fields.Many2one('x.master.modul', string='Modul')
    name = fields.Char()


class master_sumber(models.Model):
    _name = 'x.master.sumber'

    name = fields.Char(string="Name")

class problem_categ(models.Model):
    _name = 'x.problem.categ'

    name = fields.Char(string="Category Problem")


class master_question(models.Model):
    _name = 'x.master.question'

    name = fields.Char(string='Question')

class master_modul_dev(models.Model):
    _name = 'x.master.modul'

    name = fields.Char(string='Modul Name')


