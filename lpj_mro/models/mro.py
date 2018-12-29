# -*- coding: utf-8 -*-
import subprocess

from odoo import models, fields, api
import time
import odoo.addons.decimal_precision as dp



class mro_mode(models.Model):
     _inherit = 'mro.order'

     x_tgl_slsai = fields.Datetime('End of Execution Date', required=True, default=time.strftime('%Y-%m-%d %H:%M:%S'))
     x_mro_downtime = fields.One2many('x.mro.downtime','x_mro_order', string = 'Downtime')

class mro_downtime(models.Model):
     _name = 'x.mro.downtime'

     x_mro_order = fields.Many2one('mro.order', string = 'MRO Order', ondelete = 'cascade')
     name = fields.Many2one('x.type.downtime', 'Type Downtime')
     x_down_start = fields.Datetime('Tanggal mulai', required=True, default=time.strftime('%Y-%m-%d %H:%M:%S'))
     x_down_end = fields.Datetime('Tanggal Selesai', required=True, default=time.strftime('%Y-%m-%d %H:%M:%S'))

class ink_coverage(models.Model):
    _name = 'x.type.downtime'

    name = fields.Text(string='Deskripsikan downtime')





