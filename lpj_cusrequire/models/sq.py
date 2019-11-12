# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, time
import odoo.addons.decimal_precision as dp
from dateutil.relativedelta import relativedelta
# from . import crm_stage


class x_sq(models.Model):
    _inherit = 'x.sales.quotation'

    # name = fields.Char(string='Code SQ')
    x_product = fields.Many2one('product.product', string='Product Name', domain=[('sale_ok', '=', True)],track_visibility='always')
    x_product_tmpl = fields.Many2one('product.template', string='Product Template', domain=[('sale_ok', '=', True)],track_visibility='always')
    x_quotation_id = fields.Many2one('sale.order')
    item_description = fields.Char(String = 'Item Name',track_visibility='always')
    x_repeat_order = fields.Boolean(default = False, string = 'Repeat Order')
    description = fields.Text(string='Description',track_visibility='always')
    # x_desc_sq = fields.Text(string='Description')
    x_status_cr = fields.Selection(
        [('draft', 'Draft'), ('SPV', 'Need Approval SPV'), ('approve', 'Approve'), ('done', 'Done'),
         ('reject', 'Reject')],
        default='draft', string='Status SQ', readonly=True)
    x_sales_id = fields.Many2one('res.partner', string='Sales',
                                 domain=[('customer', '=', False), ('supplier', '=', False)])
    x_customer_id = fields.Many2one('res.partner', string='Customer', domain=[('customer', '=', True)])
    x_request_date = fields.Date(string='Request Date', store=True, readonly=True, default=datetime.now())
    x_duedate_drawing = fields.Datetime(string='Due Date Drawing', default=datetime.now())
    x_qty = fields.Integer('Qty (pcs)')

    x_length = fields.Float('Length (mm)')
    x_width = fields.Float('Width (mm)')
    x_length_m = fields.Float(store=True,digits=dp.get_precision('Payment Terms'))
    x_width_m = fields.Float(store=True,digits=dp.get_precision('Payment Terms'))
    x_packing_category_id = fields.Many2one('x.packing.category', 'Packing Category')
    x_satuan = fields.Selection([('sheet', 'Sheet'), ('roll', 'Roll'), ('fanfold', 'Fan Fold')], string='Satuan',
                                Default='sheet')
    x_supplier_id = fields.Many2one('res.partner', string='Suplier', domain=[('supplier', '=', True)])
    x_material_type_id = fields.Many2one('product.template', 'Material Type',domain=[('categ_id.sts_bhn_utama.name', '=', 'Bahan Utama')])
    x_numbers_of_colors = fields.Integer('Number Of Color')
    x_varnish = fields.Boolean('Varnish')
    x_special_color = fields.Boolean('Special Color')
    x_ink_coverage = fields.Selection([('0.0', '0.0'), ('0.25', '0.25'), ('0.5', '0.5'), ('0.75', '0.75'), ('1', '1')],
                                       string='Ink Coverage')

    x_mrpwordkcenter_id = fields.Many2one('mrp.workcenter', 'Prime Machine')
    x_lamination = fields.Boolean('Lamination')
    x_category_foil = fields.Many2one('x.category.finishing.process', string='Category Foil')
    x_reg_cr_mkt = fields.Boolean('Request Color Range')
    x_jumlah_cr_mkt = fields.Integer('Request Color Range Count')

    x_reg_cr_pde = fields.Boolean('Request Color Range', related="x_product.x_reg_cr_pde_m")
    x_jumlah_cr_pde = fields.Integer('Request Color Range Count', related="x_product.x_jumlah_cr_pde_m")
    start_of_date = fields.Date(string='Price Start Date', readonly=True)
    end_of_date = fields.Date(string='Price End Date', compute='end_date_function')
    compute_field = fields.Boolean(string="check field", compute="get_user")
    x_is_salemanager = fields.Boolean(string="check field apakah sales manager", compute="cek_sales_manager")
    x_price_low = fields.Float('Price Low', digits=dp.get_precision('Prroduct Price'))
    x_price_high = fields.Float('Price High', digits=dp.get_precision('Prroduct Price'))
    x_price_fix = fields.Float('Price Approve', digits=dp.get_precision('Prroduct Price'))
    x_hpp = fields.Float('HPP', readonly=True, digits=dp.get_precision('Prroduct Price'))
    x_harga_repeat = fields.Float(readonly=True, string='Harga Repeat')
    x_req_dk = fields.Datetime(string='Request Duedate Kirim',track_visibility='always', required = True)
    x_tgl_request = fields.Datetime(string='Tanggal Request', readonly = True)
    x_flag_reqdk = fields.Boolean(string='Sudah Direquest dk ?', default = False)
    x_flag_appdk = fields.Boolean(string='Sudah Diapprove dk ?', default=False)
    x_is_salemanager = fields.Boolean(string="check field apakah sales manager", compute="cek_sales_manager")
    x_status_dk = fields.Selection(
        [('draft', 'Draft'),('requested', 'Requested'), ('reject', 'Reject'), ('approve', 'Approve')],
        default='draft', string='Status Request Duedate Kirim', readonly=True,track_visibility='always')



    @api.one
    def cek_sales_manager(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('sales_team.group_sale_manager'):
            self.x_is_salemanager = True
        else:
            self.x_is_salemanager = False

    @api.multi
    def act_req_dk(self):
        x_approval_dk = self.env['x.approval.dk']
        self.x_flag_reqdk = True
        self.x_status_dk = 'requested'
        self.x_tgl_request = datetime.now()
        x_approval_dk.create({
            'name': self.id,
            'x_sales': self.x_sales_id.id,
            'x_flag_reqdk':True,
            'x_customer': self.x_customer_id,
            'x_item':self.item_description,
            'x_qty': self.x_qty,
            'x_tgl_kirim': self.x_req_dk,
            'x_mesin': self.x_mrpwordkcenter_id,
        })


    @api.onchange("x_length", "x_width")
    def check_konversi(self):
        if self.x_length > 0:
            self.x_length_m = self.x_length / 1000
        if self.x_width > 0:
            self.x_width_m = self.x_width / 1000

    # @api.multi
    # def act_approve(self):
    #     self.x_status_cr = 'approve'

    @api.multi
    def act_reject(self):
        self.x_status_cr = 'reject'
        self.x_flag_reqdk = False
        self.x_flag_appdk = False
        self.x_status_dk = 'reject'
        self.state = '9'
        ac = self.env['ir.model.data'].xmlid_to_res_id('lpj_cusrequire.reject_reason_form', raise_if_not_found=True)
        # for o in self:
        sq = self.name

        result = {
            'name': 'Reject Reason',
            'view_type': 'form',
            'res_model': 'x.reject.reason',
            'view_id': ac,
            'context': {
                'default_name': sq
            },
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'new',
        }
        return result


    @api.one
    def cek_sales_manager(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('sales_team.group_sale_manager'):
            self.x_is_salemanager = True
        else:
            self.x_is_salemanager = False

    @api.one
    def get_user(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('account.group_account_manager'):
            self.compute_field = True
        else:
            self.compute_field = False
    @api.one
    def end_date_function(self):
        # Menambah end of date + 60 hari
        start_date = self.start_of_date

        if start_date != False:
            jumlah_hari = '90'
            date_format = '%Y-%m-%d'
            date = self.start_of_date

            start_date_var = datetime.strptime(str(date), date_format)
            end_date_var = start_date_var + relativedelta(days=int(jumlah_hari))
            self.end_of_date = str(end_date_var)


    @api.onchange('x_jumlah_cr_mkt', 'x_reg_cr_mkt', 'x_repeat_order', 'x_product')
    def _update_reg_cr(self):
        if self.x_repeat_order and self.x_reg_cr_mkt:
            self.x_reg_cr_pde = self.x_reg_cr_mkt
            self.x_jumlah_cr_pde = self.x_jumlah_cr_mkt

        if self.x_reg_cr_mkt == False:
            self.x_reg_cr_pde = False
            # self.update({'x_reg_cr_pde': False})

        product = self.x_product
        marketing = self.x_reg_cr_mkt

        product_product = self.env['product.product'].search([('id', '=', product.id)])
        if product_product:
            if marketing == True:
                product_product.write({
                    'x_reg_cr_mkt_m': True,
                    'x_jumlah_cr_mkt_m': self.x_jumlah_cr_mkt,
                })
            else:
                product_product.write({
                    'x_reg_cr_mkt_m': False,
                    'x_jumlah_cr_mkt_m': self.x_jumlah_cr_mkt,
                })

    @api.model
    def create(self, vals):
        result = super(x_sq, self).create(vals)

        sequence = self.env['ir.sequence'].next_by_code('x.sales.quotation') or ('New')
        result.write({'name': sequence})

        result.write({'start_of_date': datetime.now()})

        return result

    @api.onchange("x_repeat_order")
    def check_repeat(self):
        if self.x_repeat_order == True:
            if self.x_product:
                self.env.cr.execute("select x_material_type_id, x_length, x_width, x_varnish, x_special_color,"
                                    " x_ink_coverage, x_mrpwordkcenter_id, x_lamination, x_category_foil from x_cusrequirement where "
                                    "x_product = '" + str(
                    self.x_product.id) + "'and create_date = (select max(create_date) from x_cusrequirement where x_product = '" + str(
                    self.x_product.id) + "')")
                z = self.env.cr.fetchone()
                if z:
                    self.x_material_type_id = z[0]
                    self.x_length = z[1]
                    self.x_width = z[2]
                    self.x_varnish = z[3]
                    self.x_special_color = z[4]
                    self.x_ink_coverage = z[5]
                    self.x_mrpwordkcenter_id = z[6]
                    self.x_lamination = z[7]
                    self.x_category_foil = z[8]
