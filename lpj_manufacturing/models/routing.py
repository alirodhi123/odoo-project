# -*- coding: utf-8 -*-
import subprocess

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class sale_custom(models.Model):
     _inherit = 'mrp.routing.workcenter'

     x_tcm_second = fields.Float(digits=dp.get_precision('mrp routing'),string = 'Default Duration in second')
     x_speed_per_mnt = fields.Float(string = 'Meter per Menit' , digits=(16, 4))

     @api.onchange('x_tcm_second')
     def set_value(self):
          self.time_cycle_manual = self.x_tcm_second / 60

