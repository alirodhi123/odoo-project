# -*- coding: utf-8 -*-


from odoo import models, fields, api, _


class MrpWorkOrder(models.Model):
    _inherit = 'mrp.workorder'

    wo_capacity = fields.Float(string='WC Weekly Capacity (Hours)', related='workcenter_id.wc_capacity', store='True', group_operator="avg")
    duration_expected_hours = fields.Float(string='Expected Duration (Hours)', compute='expected_duration_hours', store='True')

    @api.depends('duration_expected')
    def expected_duration_hours(self):
        workorder = self
        workorder.duration_expected_hours = (workorder.duration_expected) / 60
        return workorder.duration_expected_hours
