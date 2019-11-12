from odoo import models, fields, api


class SelfEvalKanban(models.Model):
    _name = 'x.self.evaluation.kanban'

    name = fields.Char(string="Periode Bulan")
    se_count = fields.Integer(compute='_compute_se_count')

    @api.multi
    def _compute_se_count(self):
        for o in self:
            se_data = o.env['x.self.eval'].sudo().read_group([('x_periode_id', 'in', self.ids)],
                                                                      ['x_periode_id'], ['x_periode_id'])
            result = dict((data['x_periode_id'][0], data['x_periode_id_count']) for data in se_data)
            for employee in self:
                employee.se_count = result.get(employee.id, 0)
