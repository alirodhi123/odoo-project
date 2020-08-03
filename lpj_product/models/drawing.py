# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class _drawing(models.Model):
    _name = 'x.drawing'
    _inherit = 'mail.thread'
    _description = 'Drawing'


    def _default_drawing(self):
        return self.env['res.partner'].browse(self._context.get('active_id'))


    name = fields.Char(string='Code')
    x_file = fields.Binary(string = 'Image',track_visibility='onchange')
    x_file_template = fields.Binary("Drawing with template", attachment=True,track_visibility='onchange', help="Upload file drawing with template (will send to customer)")
    x_description = fields.Char(string='Description', copy=False,track_visibility='onchange')
    x_partner = fields.Many2one('res.partner', string="Customer", track_visibility='onchange')
    x_level_dwg = fields.Many2one('x.level.drawing', string="Level Drawing")

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('x.drawing') or _('New')
        customer_id = vals['x_partner']

        partner = self.env['res.partner'].search([('id', '=', customer_id)])
        if partner:
            for row in partner:
                kode_customer = row.x_kode_customer

                if kode_customer:
                    vals['name'] = "DWG" + "-" + kode_customer + seq
                else:
                    vals['name'] = "DWG" + seq

                result = super(_drawing, self).create(vals)
                return result

class level_drawing(models.Model):
    _name = 'x.level.drawing'

    name = fields.Char(string="Level")
