# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class _drawing(models.Model):
    _name = 'x.drawing'
    _inherit = 'mail.thread'
    _description = 'Drawing'

    name = fields.Char(string='Code')
    x_file = fields.Binary(string = 'Image',track_visibility='onchange')
    x_file_template = fields.Binary("Drawing with template", attachment=True,track_visibility='onchange', help="Upload file drawing with template (will send to customer)")
    x_description = fields.Char(string='description', copy=False,track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('x.drawing') or _('New')

        result = super(_drawing, self).create(vals)
        return result
