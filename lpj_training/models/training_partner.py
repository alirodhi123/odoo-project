from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError



class res_partner_inherit(models.Model):
    _inherit = 'res.partner'

    trainer_count = fields.Integer(string="Trainer", compute='_compute_trainers_count')

    @api.multi
    def _compute_trainers_count(self):
        for o in self:
            var_trainers = self.env['x.training.schedule'].search([('trainer_id', '=', o.id)])
            if var_trainers:
                for row in var_trainers:
                    state = row.state

                    if state == 'done':
                        trainers = var_trainers.sudo().read_group([('trainer_id', 'in', self.ids)],
                                                                   ['trainer_id'],
                                                                   ['trainer_id'])
                        result = dict((data['trainer_id'][0], data['trainer_id_count']) for data in trainers)
                        for partner in self:
                            partner.trainer_count = result.get(partner.id, 0)

