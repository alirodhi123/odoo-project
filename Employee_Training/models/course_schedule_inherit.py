from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError


class course_schedule_inherit(models.Model):
    _inherit = 'course.schedule'

    def _default_id(self):
        return self.env['training.training'].browse(self._context.get('active_id'))

    x_training_id = fields.Many2one('training.training', string="Training Id", default=_default_id)