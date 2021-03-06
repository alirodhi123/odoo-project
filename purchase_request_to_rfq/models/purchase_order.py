# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

from odoo import _, api, exceptions, fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta
import odoo.addons.decimal_precision as dp


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('pending', 'Pending'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')
    x_user_approve = fields.Char(string="User Approve", compute='_get_user_approve')

    @api.multi
    def _purchase_request_confirm_message_content(self, request,
                                                  request_dict):
        self.ensure_one()
        if not request_dict:
            request_dict = {}
        title = _('Order confirmation %s for your Request %s') % (
            self.name, request.name)
        message = '<h3>%s</h3><ul>' % title
        message += _('The following requested items from Purchase Request %s '
                     'have now been confirmed in Purchase Order %s:') % (
            request.name, self.name)

        for line in request_dict.values():
            message += _(
                '<li><b>%s</b>: Ordered quantity %s %s, Planned date %s</li>'
            ) % (line['name'],
                 line['product_qty'],
                 line['product_uom'],
                 line['date_planned'],
                 )
        message += '</ul>'
        return message

    @api.multi
    def _purchase_request_confirm_message(self):
        request_obj = self.env['purchase.request']
        for po in self:
            requests_dict = {}
            for line in po.order_line:
                for request_line in line.sudo().purchase_request_lines:
                    request_id = request_line.request_id.id
                    if request_id not in requests_dict:
                        requests_dict[request_id] = {}
                    date_planned = "%s" % line.date_planned
                    data = {
                        'name': request_line.name,
                        'product_qty': line.product_qty,
                        'product_uom': line.product_uom.name,
                        'date_planned': date_planned,
                    }
                    requests_dict[request_id][request_line.id] = data
            for request_id in requests_dict:
                request = request_obj.sudo().browse(request_id)
                message = po._purchase_request_confirm_message_content(
                    request, requests_dict[request_id])
                request.message_post(body=message, subtype='mail.mt_comment')
        return True

    @api.multi
    def _purchase_request_line_check(self):
        for po in self:
            for line in po.order_line:
                for request_line in line.purchase_request_lines:
                    if request_line.sudo().purchase_state == 'done':
                        raise exceptions.Warning(
                            _('Purchase Request %s has already '
                              'been completed') % request_line.request_id.name)
        return True

    @api.multi
    def button_confirm(self):
        self._purchase_request_line_check()
        res = super(PurchaseOrder, self).button_confirm()
        self._purchase_request_confirm_message()
        return res

    @api.multi
    def print_quotation2(self):
        self.write({'state': "sent"})
        return self.env['report'].get_action(self, 'purchase_request_to_rfq.report_purchasequotation')

    @api.multi
    def print_purchase_order(self):
        return self.env['report'].get_action(self, 'purchase_request_to_rfq.report_document_po')

    # Action button pending PO / RFQ
    @api.multi
    def action_pending(self):
        self.state = 'pending'

    # Action button continue order PO / RFQ
    @api.multi
    def action_back_to_rfq(self):
        self.state = 'draft'

    # Get user approve dari mail message
    @api.one
    def _get_user_approve(self):

        self.env.cr.execute("select rp.name as users, mtv.field as field, mtv.field_desc, mtv.new_value_char "
                            "from mail_message mm "
                            "left join mail_tracking_value mtv on mm.id = mtv.mail_message_id "
                            "left join res_users ru on mm.write_uid = ru.id "
                            "left join res_partner rp on ru.partner_id = rp.id "
                            "where mm.model = 'purchase.order' and mm.record_name like '%" + self.name + "%'" 
                            "and mtv.new_value_char = 'Locked' "
                            "order by mtv.write_date DESC "
                            "limit 1")
        row = self.env.cr.fetchone()
        if row:
            user = row[0]
            self.x_user_approve = user
            return self.x_user_approve
        else:
            self.x_user_approve = "Novrinda Ayu"


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    x_category = fields.Float(related='product_uom.factor_inv')
    x_internal_ref = fields.Char(related='product_id.default_code')
    x_variant_po = fields.Char(readonly=True, compute = '_get_variant_po')
    x_qty_meterpersegi_po = fields.Float(string = 'Quantity (m2)', compute = '_meter_persegi', stored = True)
    x_harga_meterpersegi = fields.Float(string = 'Harga (m2)')
    price_unit = fields.Float(string='Unit Price', required=True, digits=dp.get_precision('Product Price'), stored = True)
    x_last_price = fields.Float(string="Last Price", readonly=True)


    @api.one
    def _get_variant_po(self):
        self.env.cr.execute("select pav.name from product_attribute_value_product_product_rel ppr "
                            "left join product_attribute_value pav on ppr.product_attribute_value_id = pav.id "
                            "left join product_attribute pa on pav.attribute_id = pa.id "
                            "left join product_product pp on ppr.product_product_id = pp.id "
                            "left join product_template pt on pp.product_tmpl_id = pt.id "
                            "where pa.name = 'Lebaran' and pp.default_code = '" + self.x_internal_ref + "'")
        o = self.env.cr.fetchone()
        if o:
            self.x_variant_po = o[0]
            self.x_variant_po = (float(self.x_variant_po) / 1000)
            return self.x_variant_po
        else:
            return None

    @api.one
    def _meter_persegi(self):
        self.x_qty_meterpersegi_po = int(self.product_qty) * float(self.x_variant_po) * self.x_category
        if float(self.x_variant_po) == 0 :
            self.x_variant_po = 1
        if self.x_category == 0 :
            self.x_category = 1
        a = float(self.x_variant_po) * self.x_category * self.x_harga_meterpersegi
        self.write({'price_unit': a})

    purchase_request_lines = fields.Many2many(
        'purchase.request.line',
        'purchase_request_purchase_order_line_rel',
        'purchase_order_line_id',
        'purchase_request_line_id',
        'Purchase Request Lines', readonly=True, copy=False)

    @api.multi
    def action_openRequestLineTreeView(self):
        """
        :return dict: dictionary value for created view
        """
        request_line_ids = []
        for line in self:
            request_line_ids += line.purchase_request_lines.ids

        domain = [('id', 'in', request_line_ids)]

        return {'name': _('Purchase Request Lines'),
                'type': 'ir.actions.act_window',
                'res_model': 'purchase.request.line',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': domain}

