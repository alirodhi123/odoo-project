from odoo import models, fields, api


class GoalSettingKanband(models.Model):
    _name = 'x.goal.setting.kanban'

    name = fields.Char(string="Periode Bulan", required=True)
    gs_count = fields.Integer(compute='_compute_gs_count')

    @api.multi
    def _compute_gs_count(self):
        for o in self:
            gs_data = o.env['x.goal.setting'].sudo().read_group([('x_periode_id', 'in', self.ids)],
                                                                   ['x_periode_id'], ['x_periode_id'])
            result = dict((data['x_periode_id'][0], data['x_periode_id_count']) for data in gs_data)
            for goal_setting in self:
                goal_setting.gs_count = result.get(goal_setting.id, 0)
