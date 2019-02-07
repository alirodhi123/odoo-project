# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp



class penawaran_cr(models.Model):
    _name = 'x.penawaran.cr'
    _inherit = 'mail.thread'
    _description = 'Penawaran Harga'

    #name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    name = fields.Char(string='Order Referance')
    origin = fields.Char(string='Source Document', help="Reference of the document that generated this sales order request.")
    client_order_ref = fields.Char(string='Customer Reference', copy=False)

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
    
    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False, default=fields.Datetime.now)
    
    validity_date = fields.Date(string='Expiration Date', readonly=True, copy=False, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        help="Manually set the expiration date of your quotation (offer), or it will set the date automatically based on the template if online quotation is installed.")
    payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', oldname='payment_term')
    create_date = fields.Datetime(string='Creation Date', readonly=True, index=True, help="Date on which sales order is created.")
    confirmation_date = fields.Datetime(string='Confirmation Date', readonly=True, index=True, help="Date on which the sale order is confirmed.", oldname="date_confirm")
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, required=True, change_default=True, index=True, track_visibility='always')
    #pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="Pricelist for current sales order.")
    order_line = fields.One2many('x.penawaran.cr.line', 'penawaran_id', string='Order Lines')
    currency_id = fields.Many2one("res.currency",string="Currency", readonly=True)

    
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('sale.order'))
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', track_visibility='always')
    
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all', track_visibility='always')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all', track_visibility='always')
    
    @api.model
    def create(self, vals):
        #if vals.get('name', _('New')) == _('New'):
         #   if 'company_id' in vals:
          #      vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('x.penawaran.cr') or _('New')
           # else:
        vals['name'] = self.env['ir.sequence'].next_by_code('x.penawaran.cr') or _('New')

        # Makes sure partner_invoice_id', 'partner_shipping_id' and 'pricelist_id' are defined
        #if any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
        #    partner = self.env['res.partner'].browse(vals.get('partner_id'))
        #    addr = partner.address_get(['delivery', 'invoice'])
        #    vals['partner_invoice_id'] = vals.setdefault('partner_invoice_id', addr['invoice'])
        #    vals['partner_shipping_id'] = vals.setdefault('partner_shipping_id', addr['delivery'])
        #    vals['pricelist_id'] = vals.setdefault('pricelist_id', partner.property_product_pricelist and partner.property_product_pricelist.id)
        
        result = super(penawaran_cr, self).create(vals)
        return result
    
    #def _prepare_procurement_group(self):
    #    return {'name': self.name}


class penawaran_cr_line(models.Model):
    _name = 'x.penawaran.cr.line'
    _description = 'Penawaran Harga Line'

    penawaran_id = fields.Many2one('x.penawaran.cr', string='Reference Penawaran', required=True, ondelete='cascade', index=True, copy=False)
    name = fields.Text(string='Description', required=True)
       
    '''@api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.penawaran_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.penawaran_id.partner_shipping_id)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
    ''' 
          
    tax_id = fields.Many2many('account.tax', string='Taxes', domain=['|', ('active', '=', False), ('active', '=', True)])
    discount = fields.Float(string='Discount (%)', digits=dp.get_precision('Discount'), default=0.0)        
    price_unit = fields.Float('Unit Price', required=True, digits=dp.get_precision('Product Price'), default=0.0)
    
    # price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', readonly=True, store=True)  
    price_subtotal = fields.Monetary(string='Subtotal', readonly=True, store=True)    
    # price_total = fields.Monetary(compute='_compute_amount', string='Total', readonly=True, store=True)
    
    product_id = fields.Many2one('x.cusrequirement', string='Product', required=True)
    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('x.qty.pproduct'), default=1.0)
    product_uom = fields.Many2one('product.uom', string='Unit of Measure')
    
    salesman_id = fields.Many2one(related='penawaran_id.user_id', store=True, string='Salesperson', readonly=True)
    
    currency_id = fields.Many2one(related='penawaran_id.currency_id', store=True, string='Currency')
    company_id = fields.Many2one(related='penawaran_id.company_id', string='Company', store=True)
    order_partner_id = fields.Many2one(related='penawaran_id.partner_id', store=True, string='Customer')
    
    
    
    
    @api.multi
    @api.onchange('product_id', 'price_unit', 'product_uom_qty')
    def product_id_change(self):
       
       if (self.name != '') or (self.price_unit != '') or (self.product_uom_qty != ''):
           self.name = self.product_id.x_status_cr
           self.price_subtotal = self.price_unit * self.product_uom_qty

    # @api.onchange('state')
    # def sq_change(self):
    #
    #     if (self.state == 'sale') or (self.price_unit != '')
    #         self.name = self.product_id.x_status_cr
    #         self.price_subtotal = self.price_unit * self.product_uom_qty
# class Quotation_CR(models.Model):
#     _inherit = 'sales.order'
#     _name = 'sales.order'
#
#     x_customer_requirement = fields.One2many('x.cusrequirement','x_quotation_id')
#     x_customer_req_filter = fields.Many2one(related='x_customer_requirement.x_customer_id')
class sales_order(models.Model):
    _inherit = 'sale.order'
    x_po_cust = fields.Char(string='PO Customer')
    x_internal_quotation = fields.Many2one('x.print.quo',string = 'Internal Quotation')
    x_internal_quotation_line = fields.Many2one('x.print.quo.line')

    # x_internal_quotation_line = fields.One2many(related = 'x_internal_quotation.x_quo_line')
    x_sq = fields.Many2one(related = 'x_internal_quotation_line.x_cusreq')
    x_is_pkp = fields.Boolean(related='partner_id.x_pkp', readonly = True)
    x_sales_external = fields.Many2one(related = 'partner_id.user_id')
    # x_termin = fields.Many2one(related = 'partner_id.x_res_termin')


class Quotation_cr_line(models.Model):
    _inherit = 'sale.order.line'
    _name = 'sale.order.line'


    product_id = fields.Many2one('product.product',readonly=True)
    order_id = fields.Many2one('sale.order',required=True,Store=True,Index=True)
    x_flag_mo = fields.Boolean(string='Sudah buat MO', default=False)
    # x_res_partner = fields.Many2one ('res.partner', string = 'Res Partner')
    # name = fields.Text('Description')
    # x_customer_filter = fields.Many2one(related='order_id.partner_id',readonly=True)
    x_customer_requirement = fields.Many2one('x.cusrequirement','SQ',required=True)
    x_product_id = fields.Many2one(related='x_customer_requirement.x_product',readonly=True)
    x_toleransi = fields.Float(string='Toleransi Pengiriman')
    x_prd_temp = fields.Many2one('product.template',string='Product Template', related = 'product_id.product_tmpl_id')
    x_uom_area = fields.Float(related="x_prd_temp.x_tot_area")
    x_m_qty = fields.Float(compute='_get_total', string="Quantity (m2)")
    #x_customer_id = fields.Many2one(related='x_customer_requirement.x_customer_id',readonly=True)
    x_pecah_harga = fields.Selection([('yes','Yes'),('no','No')], string = 'Pecah Harga')
    x_harga_jasa = fields.Float(string = 'Harga Jasa')
    x_harga_material = fields.Float (compute = '_get_mat', string = 'Harga Material')
    x_procent_jasa = fields.Float(compute = '_get_jasa',string='%Jasa')
    x_procent_material = fields.Float(compute = '_get_material',string='%Material')
    x_trial = fields.Boolean(string = 'is trial')
    x_st_cr = fields.Selection(related = 'x_customer_requirement.x_status_cr')
    # x_quoline = fields.Selection(related='x_customer_requirement.x_quo_line')
    x_duedate_kirim = fields.Datetime (string = 'Duedate kirim', required = True)

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

    @api.onchange('x_customer_requirement')
    def quo_precost(self):
        self.product_uom_qty = self.x_customer_requirement.x_qty
        self.x_trial = self.x_prd_temp.x_is_trial

    @api.onchange('x_customer_requirement','product_id')
    def select_product(self):
        self.product_id = self.x_product_id

    @api.one
    def _get_total(self):
        self.x_m_qty = (self.x_prd_temp.x_length_m * self.product_uom_qty * self.x_prd_temp.x_width_m)/0.8

    @api.one
    def _get_jasa(self):
        self.x_procent_jasa = self.x_harga_jasa / self.price_unit*100

    @api.one
    def _get_material(self):
        self.x_procent_material = ((self.price_unit - self.x_harga_jasa) / self.price_unit) * 100

    @api.one
    def _get_mat(self):
        self.x_harga_material = self.price_unit - self.x_harga_jasa