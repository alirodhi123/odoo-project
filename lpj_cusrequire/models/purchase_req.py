# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp
from datetime import datetime
from dateutil.relativedelta import relativedelta


class purchase_req(models.Model):

    _inherit = 'sale.order'
    # is_responsible = fields.Boolean(default=False)


    # Action ketika button 'Create PR' di klik
    @api.multi
    def popup_create_pr(self):
        for row in self:
            order_number = row.name
            customer = row.partner_id.id
            # product = row.product_id.id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Purchase Request',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'x.popup.message.pr',
            'target': 'new',
            'context': {
                'default_name': "Are you sure want to create Purchase Request ?",
                'default_x_customer_id': customer,

                # 'default_x_product_pr': product,
            }
        }


class pop_message_pr_pengiriman(models.Model):
    # bikin tabel baru
    _name = 'x.popup.message.pr'

    def _default_id(self):
         return self.env['sale.order'].browse(self._context.get('active_id'))

    name = fields.Char(readonly=True)
    x_no_pr = fields.Many2one('sale.order', string="Order Number", readonly=True, default=_default_id)
    x_customer_id = fields.Many2one('res.partner', string='Customer', readonly=True)

    # x_product_pr = fields.Many2one('product.product', string="Product", readonly=True)



    @api.multi
    def create_pr(self):
        ac = self.env['ir.model.data'].xmlid_to_res_id('purchase_request.view_purchase_request_form',
                                                       raise_if_not_found=True)
        for row in self:
            order_number = row.x_no_pr
            for data in order_number:
                no_so = data.id

            # order_number = row.x_no_pr.name
            # order_name = row.x_no_pr.id
            # for data in order_number:
            #     no_pr = data.id

        result = {
            'name': 'Create PR',
            'view_type': 'form',
            'res_model': 'purchase.request',
            'view_id': ac,
            'context': {
                'default_x_no_so': no_so,
            },
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'current',
        }
        return result

    @api.multi
    def dont_need_pr(self):
        id = self.x_no_pr.id

        order_number = self.env['sale.order'].search([('id', '=', id)])
        if order_number:
            order_number.write({'is_responsible': True})



