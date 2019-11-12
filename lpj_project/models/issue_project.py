# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time
from datetime import datetime, time,timedelta


class inherit_project_issue(models.Model):
    _name = 'project.issue'
    _inherit = ['project.issue', 'mail.thread']
    # _inherit = 'mail.thread'

    x_assign_dept = fields.Many2one('hr.department', string='Assign Dept')
    x_state = fields.Selection(
        [('1', 'OPEN'), ('2', 'SOLVED'), ('3', 'IMPROVED')],
        default='1', track_visibility='onchange', string="Status")

    x_duration = fields.Integer(string='Durasi (m)')
    x_reference = fields.Text(string='Reference Record')
    x_quick_solution = fields.Text(string='Quick Solution')
    x_improvement = fields.Text(string='Improvement')

    # x_duration_view = fields.Float(string="Duration (minutes)", digits=(12, 0), compute='get_duration_minutes')
    x_op_to_sol = fields.Char(string="Solved Duration ",readonly=True)
    x_date1= fields.Datetime(default=datetime.now())




    @api.multi
    def action_next(self):
        new_state = int(self.x_state) + 1
        self.x_state = str(new_state)
        if self.x_state == '2':
            self.x_date1 = datetime.now()
            format = "%Y-%m-%d %H:%M:%S"
            date1 = datetime.strptime(str(self.create_date), format)
            date2 = datetime.strptime(str(self.x_date1),format)
            d12 = date2 - date1
            self.x_op_to_sol = d12

    @api.multi
    def action_prev(self):
        new_state = int(self.x_state) - 1
        self.x_state = str(new_state)
