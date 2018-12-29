# -*- coding: utf-8 -*-

from odoo import models, fields, api

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

    # Sequences
    @api.model
    def create(self, vals):
        vals['x_name'] = self.env['ir.sequence'].next_by_code('seq.cca') or ('New')

        result = super(inherit_project_task, self).create(vals)
        return result
