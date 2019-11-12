
from odoo import models, fields, api


class MasterSelfEvaluation(models.Model):
    _name = 'x.master.self.evaluation'
    _inherit = ['mail.thread', 'ir.needaction_mixin']


    name = fields.Char(required=True)
    x_master_se_ids = fields.One2many('x.master.self.evaluation.line', 'x_master_se_id')


class MasterSelfEvaluationLine(models.Model):
    _name = 'x.master.self.evaluation.line'

    x_master_se_id = fields.Many2one('x.master.self.evaluation', ondelete='cascade')
    x_question = fields.Text(string="Master Questions")