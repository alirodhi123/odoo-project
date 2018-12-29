# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2018-TODAY NIKHIL KRISHNAN(nikhilkrishnan0101@gmail.com).
#    Author: Nikhil krishnan(nikhilkrishnan0101@gmail.com)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from itertools import groupby
from odoo import models, fields, api, _


class MultiQuotations(models.Model):
    _name = 'multi.quotations'

    @api.depends('multi_quotation_line.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.multi_quotation_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed),
                'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })

    @api.model
    def _default_note(self):
        return self.env['ir.config_parameter'].sudo().get_param(
            'sale.use_sale_note') and self.env.user.company_id.sale_note or ''

    name = fields.Char(string='Quotation Number')
    multi_order_id = fields.Many2one('sale.order', string='Order Reference', ondelete='cascade', index=True,
                                     copy=False)
    partner_id = fields.Many2one('res.partner', string='Customer')
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', required=True,
                                   help="Pricelist for current sales order.")
    company_id = company_id = fields.Many2one('res.company', string='Company', change_default=True,
                                              default=lambda self: self.env['res.company']._company_default_get('ir.attachment'))
    product_count = fields.Integer(string='Number of Products')
    multi_quotation_line = fields.One2many('multi.quotation.line', 'multi_quotation_id', string='Order Lines',
                                           copy=True, auto_join=True)
    currency_id = fields.Many2one("res.currency", related='pricelist_id.currency_id', string="Currency", readonly=True, required=True)
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', track_visibility='onchange')
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all', track_visibility='always')
    note = fields.Text('Terms and conditions', default=_default_note)

    @api.multi
    def write(self, values):
        i = 0
        if values.get('multi_quotation_line'):
            for line in values['multi_quotation_line']:
                i = i + 1
        else:
            i = 0
        values['product_count'] = i
        return super(MultiQuotations, self).write(values)

    @api.model
    def create(self, values):
        # values.update(self._prepare_add_missing_fields(values))
        sale_order_id = self.env['sale.order'].search([('id', '=', values['multi_order_id'])])
        new_name = sale_order_id.name + self.env['ir.sequence'].next_by_code('multi.quotation')
        values['name'] = new_name
        i = 0
        if values.get('multi_quotation_line'):
            for line in values['multi_quotation_line']:
                i = i + 1
        values['product_count'] = i

        if any(f not in values for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
            partner = self.env['res.partner'].browse(values.get('partner_id'))
            values['pricelist_id'] = values.setdefault('pricelist_id', partner.property_product_pricelist and partner.property_product_pricelist.id)
        return super(MultiQuotations, self).create(values)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_multi_quotation_selector(self):
        ctx = {
            'default_model': 'sale.order',
            'default_order_id': self.id,
        }

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'multi.quotations.selector',
            'view_id': self.env.ref('multiple_quotation_handler.view_multi_quotation_selector').id,
            'target': 'new',
            'context': ctx,
        }

    @api.multi
    def _get_multi_tax_amount_by_group(self, val):
        self.ensure_one()
        res = {}
        for line in val.multi_quotation_line:
            price_reduce = line.price_unit * (1.0 - line.discount / 100.0)
            taxes = line.tax_id.compute_all(price_reduce, quantity=line.product_uom_qty, product=line.product_id,
                                            partner=self.partner_shipping_id)['taxes']
            for tax in line.tax_id:
                group = tax.tax_group_id
                res.setdefault(group, {'amount': 0.0, 'base': 0.0})
                for t in taxes:
                    if t['id'] == tax.id or t['id'] in tax.children_tax_ids.ids:
                        res[group]['amount'] += t['amount']
                        res[group]['base'] += t['base']
        res = sorted(res.items(), key=lambda l: l[0].sequence)
        res = [(l[0].name, l[1]['amount'], l[1]['base'], len(res)) for l in res]
        return res

    @api.multi
    def order_lines_multi_layouted(self, val):
        """
        Returns this order lines classified by sale_layout_category and separated in
        pages according to the category pagebreaks. Used to render the report.
        """
        self.ensure_one()
        report_pages = [[]]
        for category, lines in groupby(val.multi_quotation_line, lambda l: l.layout_category_id):
            # If last added category induced a pagebreak, this one will be on a new page
            if report_pages[-1] and report_pages[-1][-1]['pagebreak']:
                report_pages.append([])
            # Append category to current report page
            report_pages[-1].append({
                'name': category and category.name or _('Uncategorized'),
                'subtotal': category and category.subtotal,
                'pagebreak': category and category.pagebreak,
                'lines': list(lines)
            })

        return report_pages

    @api.multi
    def order_lines_multiple_layouted(self):
        """
        Returns this multiple Quotation lines. Used to render the report.
        """
        self.ensure_one()
        report_pages = []
        for multi_order_line in self.multi_order_lines:
            report_pages.append(multi_order_line)
        return report_pages

    @api.multi
    def action_multiquotation(self):
        if self.is_multiquotation:
            self.is_multiquotation = False
        else:
            self.is_multiquotation = True

    @api.multi
    def action_quotation_send(self):
        '''
        This function opens a window to compose an email, with the edi sale template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        name_set = ""
        amount_set = ""
        if self.is_multiquotation:
            name_set = "("
            amount_set = "["
            for lines in self.multi_order_lines:
                name_set = name_set + lines.name + ","
                amount_set = amount_set + str(lines.amount_total) + " " + str(self.currency_id.symbol) + ", "
            try:
                template_id = ir_model_data.get_object_reference('multiple_quotation_handler', 'email_template_multi_quotation')[1]
            except ValueError:
                template_id = False
        else:
            try:
                template_id = ir_model_data.get_object_reference('sale', 'email_template_edi_sale')[1]
            except ValueError:
                template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "sale.mail_template_data_notification_email_sale_order",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            'origin_name': name_set,
            'origin_amount': amount_set
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    is_multiquotation = fields.Boolean(string='Enable multi-Quotation', readonly=True)
    multiquotation_note = fields.Text(string='Quotation Note', help="Report footer Note", default='Decision is yours, choose the best.')
    multi_order_lines = fields.One2many('multi.quotations', 'multi_order_id', string='Order Lines', copy=True)


class MultiQuotationOrderLine(models.Model):
    _name = 'multi.quotation.line'
    _inherit = ['sale.order.line']

    multi_quotation_id = fields.Many2one('multi.quotations', string='Order Reference', copy=False)
    order_id = fields.Many2one('sale.order', string='Order Reference', ondelete='cascade', index=True,
                               copy=False)
