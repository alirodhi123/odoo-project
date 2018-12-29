# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.tools import amount_to_text_en
from odoo.tools import amount_to_text

class kuitansi_line(models.Model):
    _name = 'x.down.payment'

    name = fields.Many2one('account.invoice')


class sale_order(models.Model):
    _inherit = 'sale.order'

    is_responsible = fields.Boolean(string="DP Status", default=False)

    @api.model
    def create(self, vals):
        res = super(sale_order, self).create(vals)

        id_cus = vals['partner_id']
        customer = self.env['x.due.date.pembayaran'].search([('x_customer', '=', id_cus)])


        return res
