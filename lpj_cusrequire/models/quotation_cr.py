# -*- coding: utf-8 -*-
import datetime
from odoo import models, fields, api
import odoo.addons.decimal_precision as dp



# class penawaran_cr(models.Model):
#     _name = 'x.penawaran.cr'
#     _inherit = 'mail.thread'
#     _description = 'Penawaran Harga'
#
#     name = fields.Char(string='Order Referance')
#     origin = fields.Char(string='Source Document', help="Reference of the document that generated this sales order request.")
#     client_order_ref = fields.Char(string='Customer Reference', copy=False)
#
#     state = fields.Selection([
#         ('draft', 'Quotation'),
#         ('sent', 'Quotation Sent'),
#         ('sale', 'Sales Order'),
#         ('done', 'Locked'),
#         ('cancel', 'Cancelled'),
#         ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
#
#     date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False, default=fields.Datetime.now)
#
#     validity_date = fields.Date(string='Expiration Date', readonly=True, copy=False, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
#         help="Manually set the expiration date of your quotation (offer), or it will set the date automatically based on the template if online quotation is installed.")
#     payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', oldname='payment_term')
#     create_date = fields.Datetime(string='Creation Date', readonly=True, index=True, help="Date on which sales order is created.")
#     confirmation_date = fields.Datetime(string='Confirmation Date', readonly=True, index=True, help="Date on which the sale order is confirmed.", oldname="date_confirm")
#     user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange', default=lambda self: self.env.user)
#     partner_id = fields.Many2one('res.partner', string='Customer', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, required=True, change_default=True, index=True, track_visibility='always')
#     order_line = fields.One2many('x.penawaran.cr.line', 'penawaran_id', string='Order Lines')
#     currency_id = fields.Many2one("res.currency",string="Currency", readonly=True)
#
#
#     company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('sale.order'))
#     amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', track_visibility='always')
#
#     amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all', track_visibility='always')
#     amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all', track_visibility='always')
#
#     @api.model
#     def create(self, vals):
#         vals['name'] = self.env['ir.sequence'].next_by_code('x.penawaran.cr') or _('New')
#
#         result = super(penawaran_cr, self).create(vals)
#         return result
#
#
# class penawaran_cr_line(models.Model):
#     _name = 'x.penawaran.cr.line'
#     _description = 'Penawaran Harga Line'
#
#     penawaran_id = fields.Many2one('x.penawaran.cr', string='Reference Penawaran', required=True, ondelete='cascade', index=True, copy=False)
#     name = fields.Text(string='Description', required=True)
#
#     '''@api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
#     def _compute_amount(self):
#         """
#         Compute the amounts of the SO line.
#         """
#         for line in self:
#             price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
#             taxes = line.tax_id.compute_all(price, line.penawaran_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.penawaran_id.partner_shipping_id)
#             line.update({
#                 'price_tax': taxes['total_included'] - taxes['total_excluded'],
#                 'price_total': taxes['total_included'],
#                 'price_subtotal': taxes['total_excluded'],
#             })
#     '''
#
#     tax_id = fields.Many2many('account.tax', string='Taxes', domain=['|', ('active', '=', False), ('active', '=', True)])
#     discount = fields.Float(string='Discount (%)', digits=dp.get_precision('Discount'), default=0.0)
#     price_unit = fields.Float('Unit Price', required=True, digits=dp.get_precision('Product Price'), default=0.0)
#
#     # price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', readonly=True, store=True)
#     price_subtotal = fields.Monetary(string='Subtotal', readonly=True, store=True)
#     # price_total = fields.Monetary(compute='_compute_amount', string='Total', readonly=True, store=True)
#
#     product_id = fields.Many2one('x.cusrequirement', string='Product', required=True)
#     product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('x.qty.pproduct'), default=1.0)
#     product_uom = fields.Many2one('product.uom', string='Unit of Measure')
#
#     salesman_id = fields.Many2one(related='penawaran_id.user_id', store=True, string='Salesperson', readonly=True)
#
#     currency_id = fields.Many2one(related='penawaran_id.currency_id', store=True, string='Currency')
#     company_id = fields.Many2one(related='penawaran_id.company_id', string='Company', store=True)
#     order_partner_id = fields.Many2one(related='penawaran_id.partner_id', store=True, string='Customer')
#
#
#     @api.multi
#     @api.onchange('product_id', 'price_unit', 'product_uom_qty')
#     def product_id_change(self):
#
#        if (self.name != '') or (self.price_unit != '') or (self.product_uom_qty != ''):
#            self.name = self.product_id.x_status_cr
#            self.price_subtotal = self.price_unit * self.product_uom_qty
#
#
#     state = fields.Selection([
#         ('draft', 'Quotation'),
#         ('sent', 'Quotation Sent'),
#         ('sale', 'Sales Order'),
#         ('done', 'Locked'),
#         ('cancel', 'Cancelled'),
#         ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
#
#     date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False, default=fields.Datetime.now)
#
#     validity_date = fields.Date(string='Expiration Date', readonly=True, copy=False, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
#         help="Manually set the expiration date of your quotation (offer), or it will set the date automatically based on the template if online quotation is installed.")
#     payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', oldname='payment_term')
#     create_date = fields.Datetime(string='Creation Date', readonly=True, index=True, help="Date on which sales order is created.")
#     confirmation_date = fields.Datetime(string='Confirmation Date', readonly=True, index=True, help="Date on which the sale order is confirmed.", oldname="date_confirm")
#     user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange', default=lambda self: self.env.user)
#     partner_id = fields.Many2one('res.partner', string='Customer', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, required=True, change_default=True, index=True, track_visibility='always')
#     #pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="Pricelist for current sales order.")
#     order_line = fields.One2many('x.penawaran.cr.line', 'penawaran_id', string='Order Lines')
#     currency_id = fields.Many2one("res.currency",string="Currency", readonly=True)
#
#
#     company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('sale.order'))
#     amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', track_visibility='always')
#
#     amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all', track_visibility='always')
#     amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all', track_visibility='always')
#
#     @api.model
#     def create(self, vals):
#         #if vals.get('name', _('New')) == _('New'):
#          #   if 'company_id' in vals:
#           #      vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('x.penawaran.cr') or _('New')
#            # else:
#         vals['name'] = self.env['ir.sequence'].next_by_code('x.penawaran.cr') or _('New')
#
#         # Makes sure partner_invoice_id', 'partner_shipping_id' and 'pricelist_id' are defined
#         #if any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
#         #    partner = self.env['res.partner'].browse(vals.get('partner_id'))
#         #    addr = partner.address_get(['delivery', 'invoice'])
#         #    vals['partner_invoice_id'] = vals.setdefault('partner_invoice_id', addr['invoice'])
#         #    vals['partner_shipping_id'] = vals.setdefault('partner_shipping_id', addr['delivery'])
#         #    vals['pricelist_id'] = vals.setdefault('pricelist_id', partner.property_product_pricelist and partner.property_product_pricelist.id)
#
#         result = super(penawaran_cr, self).create(vals)
#         return result


class sales_order(models.Model):
    _inherit = 'sale.order'

    x_po_cust = fields.Char(string='PO Customer')
    x_internal_quotation = fields.Many2one('x.print.quo',string = 'Internal Quotation')
    x_internal_quotation_line = fields.Many2one('x.print.quo.line')
    x_is_pkp = fields.Boolean(related='partner_id.x_pkp', readonly = True)
    x_sales_external = fields.Many2one(related = 'partner_id.user_id')
    is_block = fields.Selection([('no', 'Block'), ('yes', 'Open')], string="Customer Status", readonly=True)

    # Button Insert SQ
    # Auti filled in order line
    @api.multi
    def insert_sq(self):
        internal_quitation = self.x_internal_quotation

        print_quo = self.env['x.print.quo'].search([('id', '=', internal_quitation.id)])
        terms = []
        if print_quo:
            for row in print_quo.x_quo_line:
                values = {}
                product = row.x_prod
                # Jika product yang ada di sph kosong
                if product.active != False:
                    values['x_customer_requirement'] = row.x_cusreq.name
                    values['product_id'] = row.x_prod
                    values['product_uom_qty'] = row.x_qty
                    values['price_unit'] = row.x_price_pcs
                    terms.append((0, 0, values))

            return self.update({'order_line': terms})


class Quotation_cr_line(models.Model):
    _inherit = 'sale.order.line'
    _name = 'sale.order.line'

    product_id = fields.Many2one('product.product', readonly=True)
    order_id = fields.Many2one('sale.order', required=True, Store=True, Index=True)
    x_flag_mo = fields.Boolean(string='Sudah buat MO', default=False)
    x_customer_requirement = fields.Char('SQ', required=True)
    x_toleransi = fields.Float(string='Toleransi Pengiriman')
    x_prd_temp = fields.Many2one('product.template', string='Product Template', related='product_id.product_tmpl_id')
    x_uom_area = fields.Float(related="x_prd_temp.x_tot_area")
    x_m_qty = fields.Float(string="Quantity (m2)", compute='_get_total')
    x_pecah_harga = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Pecah Harga')
    x_harga_jasa = fields.Float(string='Harga Jasa')
    x_harga_material = fields.Float(string='Harga Material', compute='_get_mat')
    x_procent_jasa = fields.Float(string='%Jasa', compute='_get_jasa')
    x_procent_material = fields.Float(string='%Material', compute='_get_material')
    x_trial = fields.Boolean(string='is trial')
    x_st_cr = fields.Selection([('draft', 'Draft'), ('SPV', 'Need Approval SPV'), ('approve', 'Approve'), ('done', 'Done'),
                             ('reject', 'Reject')], default='draft', string='Status SQ', compute='update_status_cr')
    x_duedate_kirim = fields.Datetime(string='Duedate kirim', required=True)

    @api.model
    def create(self, vals):
        vals['x_trial'] = False
        result = super(Quotation_cr_line, self).create(vals)
        return result

    @api.model
    def create(self, vals):
        vals['x_st_cr'] = 'done'
        result = super(Quotation_cr_line, self).create(vals)
        return result

    # Update state status cr di cusrequirement
    @api.one
    def update_status_cr(self):
        sq_name = self.x_customer_requirement
        internal_quotation = self.order_id.x_internal_quotation
        state_so = self.order_id.state

        # Function cek SPH
        sph = self.env['x.print.quo'].search([('id', '=', internal_quotation.id)])
        if sph:
            if state_so == "done" or state_so == "sale":
                sph.write({'is_responsible': True})

        # Function cek SQ
        sq = self.env['x.cusrequirement'].search([('name', '=', sq_name)])
        if sq:
            if state_so == "done" or state_so == "sale":
                sq.write({'x_status_cr': 'done'})

        return True


    # Untuk menghitung quantiti meter persegi yg ada di order line
    @api.one
    def _get_total(self):
        product_uom_qty = self.product_uom_qty
        product_id = self.product_id
        product = self.env['product.product'].search([('id', '=', product_id.id)])
        if product:
            for row in product:
                lenght = row.x_length / 1000
                width = row.x_width / 1000

                meter_persegi = (lenght * product_uom_qty * width) / 0.8
                self.x_m_qty = meter_persegi


    # Untuk menghitung procent jasa
    @api.one
    def _get_jasa(self):
        for row in self:
            harga_jasa = row.x_harga_jasa
            price_unit = row.price_unit

            if price_unit != 0:
                procent_jasa = (harga_jasa / price_unit) * 100
                row.x_procent_jasa = procent_jasa

    @api.one
    def _get_material(self):
        price_unit = self.price_unit
        harga_jasa = self.x_harga_jasa

        if price_unit != 0:
            procent_material = ((price_unit - harga_jasa) / price_unit) * 100
            self.x_procent_material = procent_material

    # Untuk menghitung Harga Material
    @api.one
    def _get_mat(self):
        price_unit = self.price_unit
        harga_jasa = self.x_harga_jasa

        self.x_harga_material = price_unit - harga_jasa