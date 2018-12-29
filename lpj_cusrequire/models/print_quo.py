# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp



class print_quotation(models.Model):
    _name = 'x.print.quo'
    _inherit = 'mail.thread'

    name = fields.Char(string = 'Quotation', track_visibility='always')
    x_cust = fields.Many2one('res.partner', string = 'Customer')
    x_quo_line = fields.One2many('x.print.quo.line', 'x_quo', required=True, track_visibility='always')
    x_cusreq_quo = fields.Many2one(related = 'x_quo_line.x_cusreq')
    x_untaxed_amount = fields.Float(string='Total Harga',compute = 'total_harga' ,readonly=True, track_visibility='always')
    currency_id = fields.Many2one('res.currency')

    @api.one
    def total_harga(self):
        ab = 0
        for a in self.x_quo_line:
            a.x_total_price = a.x_price_pcs * a.x_qty
            ab += a.x_total_price
        self.x_untaxed_amount = ab

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('x.print.quo') or ('New')
        result = super(print_quotation, self).create(vals)
        return result

class print_quotation_line(models.Model):
    _name = 'x.print.quo.line'
    _inherit = 'mail.thread'

    x_quo = fields.Many2one('x.print.quo', string = 'cusreq quotation',track_visibility='always')
    x_cusreq = fields.Many2one('x.cusrequirement',string = 'Sales Quotation Code', required=True, track_visibility='always')
    x_item_desc = fields.Char(related = 'x_cusreq.item_description', track_visibility='onchange')
    x_prod = fields.Many2one(related = 'x_cusreq.x_product')
    x_qty = fields.Integer(string = 'Quantity', track_visibility='onchange')
    x_flag = fields.Boolean(related = 'x_cusreq.x_flag_quo')
    x_price_pcs = fields.Float(string = 'Harga Pcs',readonly = False, track_visibility='always')
    x_total_price = fields.Float(string = 'Total Harga')
    currency_id = fields.Many2one("res.currency", related='x_quo.currency_id', string="Currency", readonly=True,
                                  required=True)

    @api.model
    def create(self, vals):
        vals['x_flag'] = True
        result = super(print_quotation_line, self).create(vals)
        return result


    @api.onchange('x_price_pcs','x_qty')
    def harga(self):
        self.x_total_price = self.x_price_pcs * self.x_qty


class flag_quo(models.Model):
    _inherit = 'x.cusrequirement'

    x_flag_quo = fields.Boolean(string ='Internal Quotation', default = False)
    x_internal_code = fields.Char(string = 'Internal Code')
    x_quo_line_id = fields.One2many('x.print.quo.line','x_cusreq', string = 'Print Quo Line')
    x_quo_parent = fields.Many2one('x.print.quo', related = 'x_quo_line_id.x_quo')


