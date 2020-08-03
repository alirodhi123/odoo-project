# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, time
import odoo.addons.decimal_precision as dp
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
# from . import crm_stage


class x_sq(models.Model):
    _inherit = 'x.sales.quotation'


    # name = fields.Char(string='Code SQ')
    x_product = fields.Many2one('product.product', string='Product Name', domain=[('sale_ok', '=', True)],track_visibility='always')
    x_product_tmpl = fields.Many2one('product.template', string='Product Template', domain=[('sale_ok', '=', True)],track_visibility='always')
    x_quotation_id = fields.Many2one('sale.order')
    item_description = fields.Char(string = 'Item Name',track_visibility='always')
    x_repeat_order = fields.Boolean(default = False, string = 'Repeat Order')
    description = fields.Text(string='Description',track_visibility='always')
    # x_desc_sq = fields.Text(string='Description')
    x_status_cr = fields.Selection(
        [('draft', 'Draft'), ('SPV', 'Need Approval SPV'), ('approve', 'Approve'), ('done', 'Done'),
         ('reject', 'Reject')],
        default='draft', string='Status SQ', readonly=True, track_visibility='always')
    x_sales_id = fields.Many2one('res.partner', string='Sales',
                                 domain=[('customer', '=', False), ('supplier', '=', False)])
    x_customer_id = fields.Many2one('res.partner', string='Customer', domain=[('customer', '=', True)])
    x_request_date = fields.Date(string='Request Date', store=True, readonly=True, default=datetime.now())
    x_duedate_drawing = fields.Datetime(string='Due Date Drawing', default=datetime.now())
    x_qty = fields.Integer('Qty (pcs)', required = True)

    x_length = fields.Float('Length (mm)', required = True)
    x_width = fields.Float('Width (mm)', required = True)
    x_length_m = fields.Float(store=True,digits=dp.get_precision('Payment Terms'))
    x_width_m = fields.Float(store=True,digits=dp.get_precision('Payment Terms'))
    x_packing_category_id = fields.Many2one('x.packing.category', 'Packing Category')
    x_satuan = fields.Selection([('sheet', 'Sheet'), ('roll', 'Roll'), ('fanfold', 'Fan Fold')], string='Satuan',
                                Default='sheet')
    x_supplier_id = fields.Many2one('res.partner', string='Suplier', domain=[('supplier', '=', True)])
    x_material_type_id = fields.Many2one('product.template', 'Material Type',domain=[('categ_id.sts_bhn_utama.name', '=', 'Bahan Utama')])
    x_material_type_id2 = fields.Many2one('x.config.bahan', 'Material Type', required = True)
    x_numbers_of_colors = fields.Integer('Number Of Color')
    x_numbers_of_colors2 = fields.Many2one('x.config.tinta', 'Number Of Color', required = True)
    x_varnish = fields.Boolean('Varnish')
    x_special_color = fields.Boolean('Special Color')
    x_ink_coverage = fields.Selection([('0.0', '0.0'), ('0.25', '0.25'), ('0.5', '0.5'), ('0.75', '0.75'), ('1', '1')],
                                       string='Ink Coverage')

    x_mrpwordkcenter_id = fields.Many2one('mrp.workcenter', 'Prime Machine', default=1)
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
    x_req_dk_marketing = fields.Datetime(string='Request Duedate Kirim Marketing', invisible = True)
    x_tgl_request = fields.Datetime(string='Tanggal Request', readonly = True)
    x_flag_reqdk = fields.Boolean(string='Sudah Direquest dk ?', default = False)
    x_flag_appdk = fields.Boolean(string='Sudah Diapprove dk ?', default=False)
    x_is_salemanager = fields.Boolean(string="check field apakah sales manager", compute="cek_sales_manager")
    x_status_dk = fields.Selection(
        [('draft', 'Draft'),('requested', 'Requested'), ('reject', 'Reject'), ('approve', 'Approve')],
        default='draft', string='Status Request Duedate Kirim', readonly=True, track_visibility='always')
    x_id_estimated_product = fields.Many2one('x.estimated.product.crm', string="id estimated produk")
    x_id_product_repeat = fields.Many2one('x.product.repeat.crm', string="id produk repeat")
    x_id_lead = fields.Many2one('crm.lead', string="Pipeline")
    x_drawing_file_prd = fields.Binary(related="x_product.x_drawing_file", readonly = True)
    x_manufacturing_type = fields.Selection([('laprint', 'Laprint'), ('digital', 'Digital')],
                                            default='laprint', string='Manufacturing Type',
                                            track_visibility='always', required=True)
    x_planning_type = fields.Selection([('forward', 'Forward Planning'), ('backward', 'Backward Planning')],
                                       default='forward', string='Planning Type',
                                       track_visibility='always', required=True)
    x_harga_renego = fields.Float('Harga SQ', track_visibility='always', digits=dp.get_precision('Prroduct Price'))
    x_state_renego = fields.Selection(
        [('1', 'Draft'), ('2', 'Precost'), ('3', 'Approval GM'), ('4', 'Pricing GM'), ('5', 'Approval SPV'),
         ('6', 'Approve'), ('7', 'Reject'), ('8', 'Dibawah MOQ')], track_visibility='always', default='1')
    x_range_price_sq = fields.One2many('x.range.price.sq', 'x_sq')
    x_history_sq = fields.One2many('x.history.sq', 'x_sq')
    x_summary_precosting = fields.One2many('x.summary.precosting', 'x_sq', string=" ")
    x_summary_precosting_repeat = fields.One2many('x.summary.precosting.repeat', 'x_sq', string=" ")
    x_summary_precosting_low = fields.One2many('x.summary.precosting.low', 'x_sq', string=" ")
    x_summary_precosting_high = fields.One2many('x.summary.precosting.high', 'x_sq', string=" ")
    x_cek_raymond = fields.Boolean(compute="get_id")
    x_product_type_precost = fields.Many2one('x.product.type.precost', string="Product Type", required = True)
    x_ids_feature = fields.Many2many('x.feature.cost.precost', string="Feature", required = True)
    # x_ids_feature2 = fields.Many2many('x.feature.cost.precost', 'x_feature_cost_precost_x_sales_quotation_rel',
    #                                  'x_sales_quotation_id', 'x_feature_cost_precost_id', string="Feature 2", copy=False, default = True)
    x_category_precost = fields.Integer(string='Kategori')
    x_price_level = fields.One2many('x.price.level', 'x_sq')
    x_history_win = fields.One2many('x.history.sq.win', 'x_sq', string=" ")
    x_history_lost = fields.One2many('x.history.sq.lost', 'x_sq', string=" ")
    x_history_pending = fields.One2many('x.history.sq.pending', 'x_sq', string=" ")
    x_hpp_pcs = fields.Float('Hpp pcs', compute = "get_hpp")
    x_hpp_m2 = fields.Float('Hpp m2', compute="get_hpp")
    x_qty_m2 = fields.Float('Qty m2', compute="get_hpp")
    x_price_total = fields.Integer('Harga Standart Total', compute="get_hpp")
    x_profit_standart = fields.Char('Profit Standart', compute="get_hpp")
    x_renego_total = fields.Integer('Harga Renego Total', compute="get_hpp")
    x_profit_renego = fields.Char('Profit Renego', compute="get_hpp")
    x_m2_standart = fields.Integer('Harga Std/m2', compute="get_hpp")
    x_m2_renego = fields.Integer('Harga Renego/m2', compute="get_hpp")
    x_harga_renego2 = fields.Float('Harga SQ', digits=dp.get_precision('Prroduct Price'), related="x_harga_renego", readonly=True)
    x_renego_total2 = fields.Integer('Harga Renego Total', related="x_renego_total", readonly=True)
    x_profit_renego2 = fields.Char('Profit Renego', related="x_profit_renego", readonly=True)
    x_hpp_total = fields.Integer('Hpp Total', compute="get_hpp")
    x_price_high2 = fields.Float('Harga Standart/pcs', digits=dp.get_precision('Prroduct Price'),related="x_price_high", readonly=True)

    x_total_cost_hpp = fields.Integer(string='Total Cost Hpp')
    x_cost_pcs_hpp = fields.Float(string='Cost/pcs Hpp')
    x_cost_m2_hpp = fields.Float(string='Cost/m2 Hpp')

    x_total_cost_low = fields.Integer(string='Total Cost Low')
    x_cost_pcs_low = fields.Float(string='Cost/pcs Low')
    x_cost_m2_low = fields.Float(string='Cost/m2 Low')

    x_total_cost_high = fields.Integer(string='Total Cost High')
    x_cost_pcs_high = fields.Float(string='Cost/pcs High')
    x_cost_m2_high = fields.Float(string='Cost/m2 High')

    x_note_moq = fields.Text(string= ' ', default='Item ini DIBAWAH MOQ m2, Silahkan Minta Harga Digital Ke Tim Digital')

    @api.one
    def get_hpp(self):
        self.x_renego_total = self.x_harga_renego*self.x_qty

        id = self.id
        self.x_hpp_pcs = self.x_cost_pcs_hpp
        self.x_hpp_m2 = self.x_cost_m2_hpp
        self.x_hpp_total = self.x_total_cost_hpp
        if self.x_harga_renego != 0 and self.x_price_high != 0:
            x_profit = round(((self.x_harga_renego - self.x_cost_pcs_hpp) / self.x_harga_renego * 100), 2)
            self.x_profit_renego = str(x_profit) + " %"
            x_profit2 = round(((self.x_price_high - self.x_cost_pcs_hpp) / self.x_price_high * 100), 2)
            self.x_profit_standart = str(x_profit2) + " %"

            # self.env.cr.execute("select x_cost_pcs,x_cost_m2,x_total_cost from x_summary_precosting "
            #                     "where name = 'Total COGS (HPP)' and x_sq = '" + str(id) + "'")
            #
            # sql = self.env.cr.fetchone()
            # if sql:
            #     self.x_hpp_pcs = x_cost_pcs_hpp
            #     self.x_hpp_m2 = x_cost_m2_hpp
            #     self.x_hpp_total = x_total_cost_hpp
            #     x_profit = round(((self.x_harga_renego-sql[0])/self.x_harga_renego * 100),2)
            #     self.x_profit_renego = str(x_profit) + " %"
            #     x_profit2 = round(((self.x_price_high-sql[0])/self.x_price_high * 100),2)
            #     self.x_profit_standart = str(x_profit2) + " %"
            # else:
            #     self.x_hpp_pcs = 0
            #     self.x_hpp_pcs = 0
            #     self.x_profit_renego = 0
            #     self.x_profit_standart = 0

            self.env.cr.execute("select round(cast(x_area_m2_tot as numeric), 2) from x_history_precosting "
                                "where x_id_sq = '" + str(id) + "'")

            sql2 = self.env.cr.fetchone()
            if sql2:
                self.x_qty_m2 = sql2[0]
                self.x_m2_renego = self.x_renego_total/sql2[0]
            else:
                self.x_qty_m2 = 0

            self.x_price_total = self.x_total_cost_high
            self.x_m2_standart = self.x_cost_m2_high

        # self.env.cr.execute("select x_cost_pcs,x_cost_m2,x_total_cost,round(cast(x_cost_margin_hpp as numeric), 2) from x_summary_precosting "
        #                     "where name = 'Total Sales Price High' and x_sq = '" + str(id) + "'")
        #
        # sql3 = self.env.cr.fetchone()
        # if sql3:
        #     self.x_price_total = sql3[2]
        #     self.x_m2_standart = sql3[1]

    @api.one
    def get_id(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('base.group_system'):
            self.x_cek_raymond = True
        else:
            self.x_cek_raymond = False

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
        self.x_req_dk_marketing = self.x_req_dk

        id = self.id
        self.env.cr.execute("select id from x_approval_dk "
                            "where name = '" + str(id) + "'")

        sql = self.env.cr.fetchone()
        if sql:
            self.x_flag_appdk = False
            x_approval_dk.update({
                'name': self.id,
                'x_sales': self.x_sales_id.id,
                'x_flag_reqdk': True,
                'x_customer': self.x_customer_id,
                'x_item': self.item_description,
                'x_qty': self.x_qty,
                'x_tgl_kirim': self.x_req_dk,
                'x_mesin': self.x_mrpwordkcenter_id,
                'x_manufacturing_type': self.x_manufacturing_type,
                'x_planning_type': self.x_planning_type,
            })
        else:
            x_approval_dk.create({
                'name': self.id,
                'x_sales': self.x_sales_id.id,
                'x_flag_reqdk': True,
                'x_customer': self.x_customer_id,
                'x_item': self.item_description,
                'x_qty': self.x_qty,
                'x_tgl_kirim': self.x_req_dk,
                'x_mesin': self.x_mrpwordkcenter_id,
                'x_manufacturing_type': self.x_manufacturing_type,
                'x_planning_type': self.x_planning_type,
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
        x_kuantitas = self.x_qty
        x_renego = self.x_harga_renego
        x_id = self.id
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        action = 'reject'

        sql = self.env.cr.execute("select renego_precost('" + str(res_user.id) +
                                  "','" + str(x_id) + "','" + str(x_kuantitas) + "','" + str(x_renego) + "','" + str(
            action) + "');")

        self.x_status_cr = 'reject'
        self.x_flag_reqdk = False
        self.x_flag_appdk = False
        self.x_status_dk = 'reject'
        self.x_state_renego = '7'
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

        id_estimated = vals['x_id_estimated_product']
        if id_estimated:
            estimated_obj = self.env['x.estimated.product.crm'].search([('id', '=', id_estimated)])
            if estimated_obj:
                estimated_obj.write({'x_flag_harga': True})
                # estimated_obj.write({'x_sq': sequence})
        else:
            id_estimated = vals['x_id_product_repeat']
            estimated_obj = self.env['x.product.repeat.crm'].search([('id', '=', id_estimated)])
            if estimated_obj:
                estimated_obj.write({'x_flag_harga': True})

        x_id = result.id
        feat_default = 12
        x_prod = result.x_product.id

        if x_prod:
            result.env.cr.execute(
                "select quot.id sq_id, x_feature_cost_precost_id feature_id from x_sales_quotation quot join x_feature_cost_precost_x_sales_quotation_rel rel on rel.x_sales_quotation_id = quot.id where "
                "x_product = '" + str(
                    x_prod) + "'and quot.id = (select max(id) from x_sales_quotation where id <> (select max(id) from x_sales_quotation where x_product = '"+str(
                    x_prod)+"') and x_product = '" + str(
                    x_prod) + "')")
            sql = result.env.cr.fetchall()
            if sql:
                if x_id:
                    result.env.cr.execute(
                        "delete from x_feature_cost_precost_x_sales_quotation_rel where x_sales_quotation_id = '" + str(
                            x_id) + "'")
                    for row in sql:
                        result.env.cr.execute(
                            "INSERT INTO x_feature_cost_precost_x_sales_quotation_rel(x_sales_quotation_id, x_feature_cost_precost_id) VALUES ('" + str(
                                x_id) + "','" + str(row[1]) + "');")

            else:
                if x_id:
                    result.env.cr.execute(
                        "delete from x_feature_cost_precost_x_sales_quotation_rel where x_sales_quotation_id = '" + str(
                            x_id) + "'")
                    result.env.cr.execute(
                        "INSERT INTO x_feature_cost_precost_x_sales_quotation_rel(x_sales_quotation_id, x_feature_cost_precost_id) VALUES ('" + str(
                            x_id) + "','" + str(feat_default) + "');")
        else:
            result.env.cr.execute(
                "delete from x_feature_cost_precost_x_sales_quotation_rel where x_sales_quotation_id = '" + str(
                    x_id) + "'")
            result.env.cr.execute(
                "INSERT INTO x_feature_cost_precost_x_sales_quotation_rel(x_sales_quotation_id, x_feature_cost_precost_id) VALUES ('" + str(
                    x_id) + "','" + str(feat_default) + "');")
        return result


    @api.onchange("x_product")
    def check_repeat(self):
        x_id = self._origin.id
        feat_default = 12
        x_prod = self.x_product.id
        if self.x_repeat_order == True:
            if self.x_product:
                self.env.cr.execute("select quot.id sq_id, x_feature_cost_precost_id feature_id from x_sales_quotation quot join x_feature_cost_precost_x_sales_quotation_rel rel on rel.x_sales_quotation_id = quot.id where "
            "x_product = '" + str(
                x_prod) + "'and quot.id = (select max(id) from x_sales_quotation where id <> (select max(id) from x_sales_quotation where x_product = '"+str(
                x_prod)+"') and x_product = '" + str(
                x_prod) + "')")
                sql = self.env.cr.fetchall()
                if sql:
                    if x_id:
                        self.env.cr.execute("delete from x_feature_cost_precost_x_sales_quotation_rel where x_sales_quotation_id = '" + str(x_id) + "'")
                        for row in sql:
                            self.env.cr.execute("INSERT INTO x_feature_cost_precost_x_sales_quotation_rel(x_sales_quotation_id, x_feature_cost_precost_id) VALUES ('" + str(x_id) + "','" + str(row[1]) + "');")

                else:
                    if x_id:
                        self.env.cr.execute(
                            "delete from x_feature_cost_precost_x_sales_quotation_rel where x_sales_quotation_id = '" + str(
                                x_id) + "'")
                        self.env.cr.execute(
                            "INSERT INTO x_feature_cost_precost_x_sales_quotation_rel(x_sales_quotation_id, x_feature_cost_precost_id) VALUES ('" + str(
                                x_id) + "','" + str(feat_default) + "');")

                self.env.cr.execute("select x_material_type_id, x_length, x_width, x_varnish, x_special_color,"
                                    " x_ink_coverage, x_mrpwordkcenter_id, x_lamination, x_category_foil,x_material_type_id2,x_numbers_of_colors,x_numbers_of_colors2, x_product_type_precost from x_sales_quotation where "
                                    "x_product = '" + str(
                    self.x_product.id) + "'and create_date = (select max(create_date) from x_sales_quotation where x_product = '" + str(
                    self.x_product.id) + "')")
                z = self.env.cr.fetchone()
                if z:
                    self.x_material_type_id = z[0]
                    if z[9]:
                        self.x_material_type_id2 = z[9]
                    else:
                        self.env.cr.execute("select id from x_config_bahan "
                                            "where name = '" + str(z[0]) + "'")

                        z2 = self.env.cr.fetchone()
                        if z2:
                            self.x_material_type_id2 = z2[0]
                    self.x_length = self.x_length
                    self.x_width = self.x_width
                    self.x_varnish = z[3]
                    self.x_special_color = z[4]
                    self.x_ink_coverage = z[5]
                    # self.x_mrpwordkcenter_id = z[6]
                    self.x_lamination = z[7]
                    self.x_category_foil = z[8]
                    if z[11]:
                        self.x_numbers_of_colors2 = z[11]
                    else:
                        self.x_numbers_of_colors2 = z[10]
                    self.x_product_type_precost = z[12]
                else:
                    self.x_material_type_id = False
                    self.x_material_type_id2 = False
                    self.x_length = self.x_length
                    self.x_width = self.x_width
                    self.x_varnish = False
                    self.x_special_color = False
                    self.x_ink_coverage = False
                    # self.x_mrpwordkcenter_id = False
                    self.x_lamination = False
                    self.x_category_foil = False
                    self.x_numbers_of_colors2 = False
                    self.x_product_type_precost = False


    @api.multi
    def action_precosting(self):
        # new_state = 2
        self.x_status_cr = 'SPV'
        # self.x_state_renego = str(new_state)
        self.color = 3
        x_nama = self.name
        x_id = self.id
        x_panjang = self.x_length
        x_lebar = self.x_width
        x_kuantitas = self.x_qty
        res_user = self.env['res.users'].search([('id', '=', self._uid)])

        sql = self.env.cr.execute("select history_precosting('"+str(res_user.id)+"','"+str(x_nama)+
                                  "','"+str(x_id)+"','"+str(x_panjang)+"','"+str(x_lebar)+"','"+str(x_kuantitas)+"');")

        self.cek_moq()

    @api.multi
    def action_renego(self):
        x_kuantitas = self.x_qty
        x_renego = self.x_harga_renego
        x_id = self.id
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        action = 'renego'

        sql = self.env.cr.execute("select renego_precost('"+str(res_user.id)+
                                  "','"+str(x_id)+"','"+str(x_kuantitas)+"','"+str(x_renego)+"','"+str(action)+"');")

        # new_state = 3
        # self.x_state_renego = str(new_state)
        # self.color = 3


    @api.multi
    def action_pricing(self):
        x_kuantitas = self.x_qty
        x_renego = self.x_harga_renego
        x_id = self.id
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        action = 'pricing'

        sql = self.env.cr.execute("select renego_precost('" + str(res_user.id) +
                                  "','" + str(x_id) + "','" + str(x_kuantitas) + "','" + str(x_renego) + "','" + str(action) + "');")

    @api.multi
    def action_confirm_dir(self):
        x_kuantitas = self.x_qty
        x_renego = self.x_harga_renego
        x_id = self.id
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        action = 'confirm_dir'

        sql = self.env.cr.execute("select renego_precost('" + str(res_user.id) +
                                  "','" + str(x_id) + "','" + str(x_kuantitas) + "','" + str(x_renego) + "','" + str(action) + "');")

    @api.multi
    def action_confirm_pricing(self):
        x_kuantitas = self.x_qty
        x_renego = self.x_harga_renego
        x_id = self.id
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        action = 'confirm_pricing'

        sql = self.env.cr.execute("select renego_precost('" + str(res_user.id) +
                                  "','" + str(x_id) + "','" + str(x_kuantitas) + "','" + str(x_renego) + "','" + str(action) + "');")

    @api.multi
    def action_confirm_spv(self):
        x_kuantitas = self.x_qty
        x_renego = self.x_harga_renego
        x_id = self.id
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        action = 'confirm_spv'

        sql = self.env.cr.execute("select renego_precost('" + str(res_user.id) +
                                  "','" + str(x_id) + "','" + str(x_kuantitas) + "','" + str(x_renego) + "','" + str(action) + "');")

    @api.multi
    def action_reject(self):
        x_kuantitas = self.x_qty
        x_renego = self.x_harga_renego
        x_id = self.id
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        action = 'reject'

        sql = self.env.cr.execute("select renego_precost('" + str(res_user.id) +
                                  "','" + str(x_id) + "','" + str(x_kuantitas) + "','" + str(x_renego) + "','" + str(action) + "');")

    @api.multi
    def reset_precosting(self):
        x_kuantitas = self.x_qty
        x_renego = self.x_harga_renego
        x_id = self.id
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        action = 'reset'

        sql = self.env.cr.execute("select renego_precost('" + str(res_user.id) +
                                  "','" + str(x_id) + "','" + str(x_kuantitas) + "','" + str(x_renego) + "','" + str(action) + "');")

    # Fungsi cek moq
    @api.multi
    def cek_moq(self):
        state_renego = self.x_state_renego
        if state_renego == 8:
            raise UserError(_('Item ini DIBAWAH MOQ m2, Silahkan Minta Harga Digital Ke Tim Digital'))





class range_price_sq(models.Model):
    _name = 'x.range.price.sq'
    name = fields.Char(string = 'Nama')
    x_sq = fields.Many2one('x.sales.quotation', string='Range Price SQ')
    x_quantity = fields.Integer(string = 'Quantity')
    x_quantity_range = fields.Char(compute='gabung', string='Quantity Range')
    x_quantity_roundup = fields.Integer(string='Quantity Roundup')
    x_quantity_m2 = fields.Integer(string='Quantity m2')
    x_price_pcs = fields.Float(string = 'Price per pcs')
    # x_price_pcs_range = fields.Char(string='Price per pcs range')
    x_price_m2 = fields.Float(string = 'Price per m2')
    x_price_total = fields.Float(string='Price Total')
    x_price_total_range = fields.Char(compute='gabung', string='Price Total')
    x_hpp_pcs = fields.Float(string='HPP per pcs')
    x_hpp_m2 = fields.Float(string='HPP per m2')
    x_hpp_total = fields.Float(string='HPP Total')
    x_hpp_total_range = fields.Char(compute='gabung', string='HPP Total')
    x_prosentase_profit = fields.Float(string = 'Prosentase Profit')
    x_hpp_total2 = fields.Float(string='HPP Total Up')
    x_price_total2 = fields.Float(string='Price Total Up')
    x_quantity_roundup2 = fields.Integer(string='Quantity Roundup Up')

    @api.one
    def gabung(self):
        x_id_r = self.id
        self.env.cr.execute("select x_sq from x_range_price_sq where id = '" + str(x_id_r) + "'")
        sql = self.env.cr.fetchone()
        id = sql[0]
        self.env.cr.execute("select max(id) from x_range_price_sq where x_sq = '"+ str(id)+"'")
        sql = self.env.cr.fetchone()
        id_range = self.id
        if sql:
            if id_range == sql[0]:
                self.x_price_total_range = 'Rp. ' + "{:,.0f}".format(self.x_price_total).replace(",",
                                                                                                 ".") + ' -- ...'
                self.x_hpp_total_range = 'Rp. ' + "{:,.0f}".format(self.x_hpp_total).replace(",",
                                                                                             ".") + ' -- ...'
                self.x_quantity_range = "{:,.0f}".format(self.x_quantity_roundup).replace(",",
                                                                                          ".") + ' -- ...'
            else:
                if self.x_price_total == 0:
                    self.x_price_total_range = 'Dibawah MOQ'
                    self.x_hpp_total_range = 'Dibawah MOQ'
                    self.x_quantity_range = "{:,.0f}".format(self.x_quantity_roundup).replace(",",
                                                                                              ".") + ' -- ' + "{:,.0f}".format(
                        self.x_quantity_roundup2).replace(",", ".")
                else:
                    self.x_price_total_range = 'Rp. ' + "{:,.0f}".format(self.x_price_total).replace(",",
                                                                                                     ".") + ' -- ' + 'Rp. ' + "{:,.0f}".format(
                        self.x_price_total2).replace(",", ".")
                    self.x_hpp_total_range = 'Rp. ' + "{:,.0f}".format(self.x_hpp_total).replace(",",
                                                                                                     ".") + ' -- ' + 'Rp. ' + "{:,.0f}".format(
                        self.x_hpp_total2).replace(",", ".")
                    self.x_quantity_range = "{:,.0f}".format(self.x_quantity_roundup).replace(",",
                                                                                                 ".") + ' -- ' + "{:,.0f}".format(
                        self.x_quantity_roundup2).replace(",", ".")

class history_sq(models.Model):
    _name = 'x.history.sq'
    x_sq = fields.Many2one('x.sales.quotation', string='History SQ')
    name = fields.Char(string = 'Action')
    x_quantity = fields.Integer(string = 'Quantity')
    x_price = fields.Float(string = 'Price')
    x_description = fields.Char(string = 'Keterangan')

class summary_precosting_repeat(models.Model):
    _name = 'x.summary.precosting.repeat'
    x_sq = fields.Many2one('x.sales.quotation', string='Summary Precosting')
    name = fields.Char(string = 'Cost Factor')
    x_total_cost = fields.Integer(string = 'Total Cost')
    x_cost_pcs = fields.Float(string = 'Cost/pcs')
    x_cost_m2 = fields.Float(string = 'Cost/m2')
    # x_profit = fields.Float(string='Profit')
    x_cost_margin_hpp = fields.Float(string='Cost Margin to HPP')
    x_cost_margin_low = fields.Float(string='Cost Margin to Price Low')

class summary_precosting(models.Model):
    _name = 'x.summary.precosting'
    x_sq = fields.Many2one('x.sales.quotation', string='Summary Precosting')
    name = fields.Char(string = 'Cost Factor')
    x_total_cost = fields.Integer(string = 'Total Cost')
    x_cost_pcs = fields.Float(string = 'Cost/pcs')
    x_cost_m2 = fields.Float(string = 'Cost/m2')
    # x_profit = fields.Float(string='Profit')
    x_cost_margin_hpp = fields.Float(string='Cost Margin to HPP')
    x_cost_margin_low = fields.Float(string='Cost Margin to Price Low')

class summary_precosting_low(models.Model):
    _name = 'x.summary.precosting.low'
    x_sq = fields.Many2one('x.sales.quotation', string='Summary Precosting Low')
    name = fields.Char(string = 'Cost Factor')
    x_total_cost = fields.Integer(string = 'Total Cost')
    x_cost_pcs = fields.Float(string = 'Cost/pcs')
    x_cost_m2 = fields.Float(string = 'Cost/m2')
    # x_profit = fields.Float(string='Profit')
    x_cost_margin_hpp = fields.Float(string='Cost Margin to HPP')
    x_cost_margin_low = fields.Float(string='Cost Margin to Price Low')

class summary_precosting_high(models.Model):
    _name = 'x.summary.precosting.high'
    x_sq = fields.Many2one('x.sales.quotation', string='Summary Precosting High')
    name = fields.Char(string = 'Cost Factor')
    x_total_cost = fields.Integer(string = 'Total Cost')
    x_cost_pcs = fields.Float(string = 'Cost/pcs')
    x_cost_m2 = fields.Float(string = 'Cost/m2')
    # x_profit = fields.Float(string='Profit')
    x_cost_margin_hpp = fields.Float(string='Cost Margin to HPP')
    x_cost_margin_low = fields.Float(string='Cost Margin to Price Low')


class price_level(models.Model):
    _name = 'x.price.level'
    x_sq = fields.Many2one('x.sales.quotation', string='Price Level')
    name = fields.Char(string = 'Cost Factor')
    x_total_cost = fields.Integer(string = 'Total Price')
    x_cost_pcs = fields.Float(string = 'Price/pcs')
    x_cost_m2 = fields.Float(string = 'Price/m2')
    x_profit = fields.Many2one('x.profit.margin.precost', string='Profit Margin')

class history_sq_win(models.Model):
    _name = 'x.history.sq.win'
    x_sq = fields.Many2one('x.sales.quotation', string='SQ')
    name = fields.Many2one('product.product', string='Product Name', domain=[('sale_ok', '=', True)])
    x_quantity = fields.Integer(string='Quantity')
    x_date = fields.Date(string='Date')
    x_total_cost = fields.Integer(string = 'Total Price')
    x_cost_pcs = fields.Float(string = 'Price/pcs')
    x_cost_m2 = fields.Float(string = 'Price/m2')
    x_profit = fields.Float(string='Profit Harga')
    x_sq_win = fields.Many2one('x.sales.quotation', string='SQ WIN')

class history_sq_lost(models.Model):
    _name = 'x.history.sq.lost'
    x_sq = fields.Many2one('x.sales.quotation', string='SQ')
    name = fields.Many2one('product.product', string='Product Name', domain=[('sale_ok', '=', True)])
    x_quantity = fields.Integer(string='Quantity')
    x_date = fields.Date(string='Date')
    x_total_cost = fields.Integer(string = 'Total Price')
    x_cost_pcs = fields.Float(string = 'Price/pcs')
    x_cost_m2 = fields.Float(string = 'Price/m2')
    x_profit = fields.Float(string='Profit Harga')
    x_sq_lost = fields.Many2one('x.sales.quotation', string='SQ LOST')


class history_sq_pending(models.Model):
    _name = 'x.history.sq.pending'
    x_sq = fields.Many2one('x.sales.quotation', string='SQ')
    name = fields.Many2one('product.product', string='Product Name', domain=[('sale_ok', '=', True)])
    x_quantity = fields.Integer(string='Quantity')
    x_date = fields.Date(string='Date')
    x_total_cost = fields.Integer(string = 'Total Price')
    x_cost_pcs = fields.Float(string = 'Price/pcs')
    x_cost_m2 = fields.Float(string = 'Price/m2')
    x_profit = fields.Float(string='Profit Harga')
    x_sq_pending = fields.Many2one('x.sales.quotation', string='SQ PENDING')


