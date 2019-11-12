# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError



class training(models.Model):
    _name = 'training.training'
    _inherit = ['mail.thread', 'ir.needaction_mixin', ]
    _rec_name = 'course_name'


    def _default_employee(self):
        return self.env.context.get('default_employee_id') or self.env['hr.employee'].search(
            [('user_id', '=', self.env.uid)], limit=1)

    # course_name = fields.Many2one(comodel_name='course.schedule', string='Course', required='1')
    name = fields.Char()
    course_name = fields.Many2one('course.schedule', string='Course')
    price_id = fields.Float(string='Price', readonly='True')
    bio_content = fields.Text(string='Contents', readonly='True')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', index=True, readonly=True,
                                  states={'new': [('readonly', False)], 'hod': [('readonly', False)]},
                                  default=_default_employee)
    bio_agrement = fields.Text(string='Agreements', readonly='True')
    # state = fields.Selection(selection=[('new', 'New'), ('hod', 'HRD Approve'), ('hrman', 'Top Management Approve'),
    #                                     ('approve', 'Approved'), ('in progress', 'In Progress'),
    #                                     ('done', 'Done'), ('reject', 'Reject')], default='new')
    state = fields.Selection(selection=[('new', 'New'), ('hod', 'HRD Approve'), ('cancel', 'Cancel')], default='new')
    user_id = fields.Many2one('res.users', string='User', related='employee_id.user_id', related_sudo=True,
                                         default=lambda self: self.env.uid, readonly=True)
    line_count = fields.Integer(string='Purchase Request Line count',compute='_compute_line_count',readonly=True)

    _track = {
        'course_name': {
            'training.mt_course_name': lambda self, cr, uid, obj, ctx=None: obj.bio_content,
        },
        'price_id': {
            'training.mt_price_id': lambda self, cr, uid, obj, ctx=None: obj.bio_content,
        },
    }

    @api.model
    def create(self, vals):
        res = super(training, self).create(vals)

        # Sequence
        sequence = self.env['ir.sequence'].next_by_code('sequence.training.new') or _('New')
        res.update({'name': sequence})

        return res

    @api.depends('x_employee_training_ids')
    def _compute_line_count(self):
        self.line_count = len(self.mapped('x_employee_training_ids'))


    @api.onchange("employee_id")
    @api.multi
    def _get_cat(self):
        schedule=self.env['course.schedule']
        list1 = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1).category_ids.ids
        schedule_ids=[]
        for sc in schedule.search([]):
            list2=sc.tags.ids
            match = any(map(lambda v: v in list1, list2))
            if match :
                schedule_ids.append(sc.id)
        return {'domain': {'course_name': [('id', 'in', schedule_ids),('state', '=', 'active')]}}


    @api.multi
    def action_new(self):
        self.state = 'new'

    @api.multi
    def action_hod(self):
        self.state = 'hod'

    @api.multi
    def action_hrman(self):
        self.state = 'hrman'

    @api.multi
    def action_approve(self):
        self.state = 'approve'

    @api.multi
    def action_in_progress(self):
        self.state = 'in progress'

    @api.multi
    def done(self):
        self.state = 'done'

    @api.multi
    def action_cancel(self):
        self.state = 'cancel'



class CourseSchedule(models.Model):
    _name = 'course.schedule'
    _inherit = ['mail.thread', 'ir.needaction_mixin', ]
    _rec_name = 'text'

    @api.one
    @api.depends('capacity', 'reserv')
    def calc_remain(self):
        if self.capacity or self.reserv:
            if self.capacity >= self.reserv:
                self.remain = self.capacity - self.reserv

    @api.multi
    def compute_reserv(self):
        calc_reserv = self.env['training.training']
        for sch in self:
            sch.reserv = calc_reserv.search_count([('course_name.id', '=', sch.id), ('state', '!=', 'cancel'),('state', '!=', 'new')])
            if sch.reserv == sch.capacity:
                sch.write({'state': 'close'})
            elif sch.reserv < sch.capacity:
                sch.write({'state':'active'})    
            return
        
        
    @api.onchange('f_date','to_date')
    def _calc_days(self):
        if self.f_date and self.to_date and self.f_date <= self.to_date:
            date_format = "%Y-%m-%d"
            start_date = datetime.strptime(self.f_date,date_format)
            end_date = datetime.strptime(self.to_date,date_format)
            res = end_date - start_date
            self.duration = str(res.days)    


    name = fields.Char()
    course_id = fields.Many2one(comodel_name='course.training', string='Course')
    duration = fields.Integer('Duration', readonly=True)
    f_date = fields.Date(string='From')
    to_date = fields.Date(string='To')
    capacity = fields.Integer(string='Capacity')
    tags = fields.Many2many('hr.employee.category', 'sch_category_rel', 'sch_id', 'category_id', string='Tags')
    price = fields.Float(string='Price', related='course_id.price_ids', readonly=True)
    trainer_id = fields.Many2one(comodel_name='partner.trainer', string='Trainer')
    # reserv = fields.Integer(string='Reservation', compute='compute_reserv')
    reserv = fields.Integer(string='Reservation')
    # remain = fields.Integer(string='Remaining', compute='calc_remain')
    remain = fields.Integer(string='Remaining')
    bio = fields.Text(string='Bio')
    state = fields.Selection(selection=[('new', 'New'), ('active', 'Active'), ('close', 'Closed')
                                        ], default='new', track_invisiblty='onchange')
    text = fields.Char(string='Cou')
    bio_cont = fields.Text('Bio')
    training = fields.One2many(comodel_name='training.training', inverse_name='course_name', string='Train')

    _track = {
        'course_id': {
            'training.mt_course_id': lambda self, cr, uid, obj, ctx=None: obj.f_date,
        },
        'trainer': {
            'training.mt_trainer': lambda self, cr, uid, obj, ctx=None: obj.f_date,
        },
    }

    @api.model
    def create(self, vals):
        res = super(CourseSchedule, self).create(vals)

        # Sequence
        sequence = self.env['ir.sequence'].next_by_code('sequence.schedule') or _('New')
        res.update({'name': sequence})

        return res

    @api.multi
    def action_new(self):
        self.state = 'new'

    @api.multi
    def action_active(self):
        self.state = 'active'

    @api.multi
    def action_close(self):
        self.state = 'close'


# ===============>>>>>>>>================<<<<<<<<<<<==============

class PartnerTrainer(models.Model):
    _name = 'partner.trainer'
    _inherit = ['mail.thread', 'ir.needaction_mixin', ]
    _rec_name = 'partner_name'

    partner_name = fields.Many2one(comodel_name='res.partner', string='Trainer', domain=[('active', '=', True)])


    _track = {
        'partner_name': {
            'training.mt_partner_name': lambda self, cr, uid, obj, ctx=None: obj.partner_name,
        },

    }


# =======================>>>>>==================<<<<<==================

class CourseTraining(models.Model):
    _name = 'course.training'
    _inherit = ['mail.thread', 'ir.needaction_mixin', ]
    _rec_name = 'course'

    course = fields.Char(string='Course Name',required='1')
    code = fields.Char(string='Code')
    bio_course = fields.Text('Bio')
    price_ids = fields.Float(string='Price',required='1')

    _sql_constraints = [
        ('course_code_unique',
         'UNIQUE(code)',
         'Code Must be Unique'),
    ]

    _track = {
        'course': {
            'training.mt_course': lambda self, cr, uid, obj, ctx=None: obj.code,
        },
        'bio': {
            'training.mt_bio': lambda self, cr, uid, obj, ctx=None: obj.code,
        },
    }


class ResPartner(models.Model):
    _inherit = 'res.partner'
    active = fields.Boolean('Is a Trainer')


# ======================================================================

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    cour_ids = fields.Selection(selection=[('new', 'New')])







