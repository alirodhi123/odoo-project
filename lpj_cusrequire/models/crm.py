# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp



class x_crm(models.Model):
    _inherit = 'crm.lead'
    x_flag_sq = fields.Boolean(default = False)
    @api.multi
    def crm_sq(self):
        self.stage_id = 2
        self.x_flag_sq = True
        ac = self.env['ir.model.data'].xmlid_to_res_id('lpj_cusrequire.requirement_form_view', raise_if_not_found=True)
        # for o in self:
        result = {
            'name': 'Sales Quotation',
            'view_type': 'form',
            'res_model': 'x.cusrequirement',
            'view_id': ac,
            'context': {
                # 'default_name': sq
            },
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'current',
        }
        return result
