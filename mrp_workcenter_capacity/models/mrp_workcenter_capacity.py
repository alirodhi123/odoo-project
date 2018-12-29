# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MrpWorkOrder(models.Model):
    _inherit = 'mrp.workcenter'

    nr_days = fields.Float(string='working days per week', required="True")
    nr_hours = fields.Float(string='working hours per day', required="True")
    nr_shift = fields.Integer(string='shifts per day', required="True")
    wc_capacity = fields.Float(string='WC Weekly Capacity (Hours)', compute='_calculate_wc_capacity', store='True', group_operator="avg")

    @api.multi
    @api.depends('nr_days','nr_hours','nr_shift','capacity','time_efficiency')
    def _calculate_wc_capacity(self):
        self.ensure_one()
        workcenter = self
        cap = 0.0
        for wc in workcenter:
            cap = wc.nr_shift * wc.nr_hours * wc.nr_days * wc.capacity * wc.time_efficiency / 100
        
        workcenter.wc_capacity = cap
        return workcenter.wc_capacity
