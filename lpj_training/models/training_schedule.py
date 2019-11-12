from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError


class TrainingSchedule(models.Model):
    _name = 'x.training.schedule'
    _inherit = 'mail.thread'
    _description = 'Training Schedule'

    def _default_id(self):
        return self.env['x.training.training'].browse(self._context.get('active_id'))

    training_id = fields.Many2one('x.training.training', string="Training Id", readonly=True, required=True, track_visibility="onchange")
    training_schedule_ids = fields.One2many('x.training.schedule.line', 'training_schedule_id',
                                            track_visibility="onchange")
    name = fields.Char()
    duration = fields.Integer('Duration', readonly=True, track_visibility="onchange")
    f_date = fields.Date(string='From', track_visibility="onchange")
    to_date = fields.Date(string='To', track_visibility="onchange")
    capacity = fields.Integer(string='Training Participants', track_visibility="onchange")
    trainer_id = fields.Many2one('res.partner', string='Trainer', track_visibility="onchange")
    reserv = fields.Integer(string='Reservation', track_visibility="onchange")
    remain = fields.Integer(string='Remaining', track_visibility="onchange")

    state = fields.Selection(selection=[('hrd', 'Need Approval'),
                                        ('direktur', 'Approval Top Management'),
                                        ('in_progress', 'In Progress'),
                                        ('data_verification', 'Data Verification'),
                                        ('done', 'Done'),
                                        ('cancel', 'Cancel')],
                             default='hrd', track_invisiblty='onchange')
    x_category_training_schedule = fields.Selection([('internal', 'Training Internal'),
                                                     ('eksternal', 'Training Eksternal')],
                                           string="Category Training", track_visibility="onchange")
    x_user_id = fields.Many2one('res.users', string='Employee', index=True, track_visibility='onchange',
                                default=lambda self: self.env.user)
    x_employee_id = fields.Many2one('hr.employee', string="Requested By", readonly=True)

    @api.model
    def create(self, vals):
        res = super(TrainingSchedule, self).create(vals)

        # Sequence
        sequence = self.env['ir.sequence'].next_by_code('sequence.x.schedule') or ('New')
        res.update({'name': sequence})

        return res

    @api.onchange('f_date', 'to_date')
    def _calc_days(self):
        if self.f_date and self.to_date and self.f_date <= self.to_date:
            date_format = "%Y-%m-%d"
            start_date = datetime.strptime(self.f_date, date_format)
            end_date = datetime.strptime(self.to_date, date_format)
            res = end_date - start_date
            self.duration = str(res.days)


    @api.multi
    def action_in_progress(self):
        category_training = self.x_category_training_schedule
        if category_training == "internal":
            self.state = 'in_progress'
        elif category_training == "eksternal":
            self.state = 'direktur'
        else:
            self.state = 'hrd'

    @api.multi
    def action_top_management(self):
        self.state = 'in_progress'

    @api.multi
    def action_data_verification(self):
        self.state = 'data_verification'

    @api.multi
    def done(self):
        self.state = 'done'

    @api.multi
    def action_cancel(self):
        self.state = 'cancel'


class TrainingScheduleLine(models.Model):
    _name = 'x.training.schedule.line'

    training_schedule_id = fields.Many2one('x.training.schedule', ondelete='cascade')
    x_name_employee = fields.Many2one('hr.employee', string="Name")
    x_work_email = fields.Char(string="Work Email")
    x_department = fields.Many2one('hr.department', string="Department")
    x_job_tittle = fields.Many2one('hr.job', string="Job Title")
    x_manager = fields.Many2one('hr.employee', string="Manager")
    x_rating = fields.Selection([('0', 'Sangat Rendah'),
                                 ('1', 'Rendah'),
                                 ('2', 'Cukup'),
                                 ('3', 'Baik'),
                                 ('4', 'Sangat Baik'),
                                 ('5', 'Luar Biasa')],
                            default='0', string="Nilai", track_invisiblty='onchange')

    # RELATED TRAINING TRAINING
    related_training_training = fields.Many2one(related='training_schedule_id.training_id')
    name = fields.Char(related='related_training_training.x_training_name')
    related_training_id = fields.Char(related='related_training_training.name', string="Training Id")
    related_category_training = fields.Selection(related='related_training_training.x_category_training')
    related_date_from = fields.Date(related='training_schedule_id.f_date')
    related_date_to = fields.Date(related='training_schedule_id.to_date')
    related_duration = fields.Integer(related='training_schedule_id.duration')
    related_trainer = fields.Many2one(related='training_schedule_id.trainer_id')