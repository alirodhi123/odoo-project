# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp

class qa_product(models.Model):
     _inherit = 'product.template'

     x_qa = fields.Boolean('QA', track_visibility='onchange')
     x_qa_measure = fields.One2many('quality.measure','x_prod',string = 'Quality Measure', track_visibility='onchange')

class quality_m(models.Model):
     _inherit = 'quality.measure'

     x_prod = fields.Many2one('product.template', string= 'Product Template', required=True, ondelete='cascade', index=True, copy=False)
