# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class prod_requirement(models.Model):
    _name = 'x.cusrequirement'
    _inherit = 'mail.thread'

    name = fields.Char(string='Code')
    item_description = fields.Char(string='Item Name', required=True, readonly=True,
                                   states={'1': [('readonly', False)]},
                                   track_visibility='always')
    description = fields.Text(track_visibility='onchange')

    color = fields.Integer('Warna')
    state = fields.Selection(
        [('1', 'Marketing'), ('2', 'Drawing'), ('3', 'Approval Cus (Drawing)'), ('4', 'PDE (Tech. Spec) '),
         ('5', 'Digital Proof'),
         ('6', 'Trial Product'), ('7', 'Approval Trial'), ('8', 'Finalize TDS'), ('9', 'Done'),
         ], default='1', track_visibility='onchange', string="Status Product")

    x_product = fields.Many2one('product.product', string='Product Name', domain=[('sale_ok', '=', True)])
    x_quotation_id = fields.Many2one('sale.order')
    x_sale_order_line_ids = fields.One2many('sale.order.line', related='x_product.x_product_sol', readonly=True)
    x_cusreq = fields.Many2one(string = 'name last SQ', related = 'x_sale_order_line_ids.x_customer_requirement')

    # x_drawing_sq = fields.Binary(string='Drawing SQ')
    # x_dwg_sq = fields.Many2one('x.drawing', string = "Drawing SQ")
    # x_harga_repeat = fields.Integer(compute = )
    x_no_so = fields.Char(string='No. SO')
    x_harga_repeat = fields.Float(readonly=True, string='Harga Repeat')
    x_tamp_tgl = fields.Integer(string='tampungan tanggal untuk loop', readonly=True)
    x_id = fields.Integer(string='tampungan tanggal untuk loop', readonly=True)
    x_request_date = fields.Date(string='Request Date',store=True, readonly = True)
    x_print = fields.Boolean(string = 'print', readonly = False)



        # for x in self.x_sale_order_line_ids:
        #     if x.id == self.x_tamp_tgl:
        #         self.x_harga_repeat = x.price_unit

    # Pre-Costing
    x_category_foil = fields.Many2one('x.category.finishing.process', string='Category Foil', readonly=True,
                                      states={'1': [('readonly', False)]})
    x_customer_id = fields.Many2one('res.partner', string='Customer', domain=[('customer', '=', True)], readonly=True,
                                    states={'1': [('readonly', False)]})

    x_ink_coverage = fields.Selection([('0.0', '0.0'), ('0.25', '0.25'), ('0.5', '0.5'), ('0.75', '0.75'), ('1', '1')],
                                      readonly=True, states={'1': [('readonly', False)]}, string='Ink Coverage')
    x_lamination = fields.Boolean('Lamination', readonly=True, states={'1': [('readonly', False)]})
    x_length = fields.Float('Length (mm)', readonly=True, states={'1': [('readonly', False)]})
    x_material_number = fields.Char('Material Number', readonly=True, states={'1': [('readonly', False)]})
    x_material_type_id = fields.Many2one('product.template', 'Material Type', readonly=True,
                                         states={'1': [('readonly', False)]}, domain=['|',('categ_id.name', '=', 'Label'),('categ_id.name', '=', 'Pita')])
    x_mrpwordkcenter_id = fields.Many2one('mrp.workcenter', 'Prime Machine', readonly=True,
                                          states={'1': [('readonly', False)]})
    x_name = fields.Char('Product Name', readonly=True, states={'1': [('readonly', False)]})
    x_numbers_of_colors = fields.Integer('Number Of Color', readonly=True, states={'1': [('readonly', False)]})
    x_packing_category_id = fields.Many2one('x.packing.category', 'Packing Category', readonly=True,
                                            states={'1': [('readonly', False)]})
    x_qty = fields.Integer('Qty (pcs)', readonly=True, states={'1': [('readonly', False)]})
    x_sales_id = fields.Many2one('res.partner', string='Sales',
                                 domain=[('customer', '=', False), ('supplier', '=', False)], readonly=True,
                                 states={'1': [('readonly', False)]})
    x_special_color = fields.Boolean('Special Color', readonly=True, states={'1': [('readonly', False)]})
    x_supplier_id = fields.Many2one('res.partner', string='Suplier', domain=[('supplier', '=', True)], readonly=True,
                                    states={'1': [('readonly', False)]})
    x_varnish = fields.Boolean('Varnish', readonly=True, states={'1': [('readonly', False)]})
    x_width = fields.Float('Width (mm)', readonly=True, states={'1': [('readonly', False)]})
    x_repeat_order = fields.Boolean('Repeat Order')
    x_status_cr = fields.Selection(
        [('draft', 'Draft'), ('SPV', 'Need Approval SPV'), ('approve', 'Approve'), ('done', 'Done'),
         ('reject', 'Reject')],
        default='draft', string='Status SQ', readonly = True)

    x_satuan = fields.Selection([('sheet', 'Sheet'), ('roll', 'Roll'), ('fanfold', 'Fan Fold')], string='Satuan',
                                Default='sheet', readonly=True,
                                states={'1': [('readonly', False)]})

    x_propose_price_low = fields.Float('Porpose Price Low', readonly=True, digits=dp.get_precision('Prroduct Price'))
    x_propose_price_high = fields.Float('Porpose Price High', readonly=True, digits=dp.get_precision('Prroduct Price'))
    x_propose_profit_low = fields.Float('Porpose Profit Low', readonly=True, digits=dp.get_precision('Prroduct Price'))
    x_propose_profit_high = fields.Float('Porpose Profit High', readonly=True,
                                         digits=dp.get_precision('Prroduct Price'))

    compute_field = fields.Boolean(string="check field", compute = "get_user")

    @api.one
    def get_user(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('account.group_account_manager'):
            self.compute_field = True
        else:
            self.compute_field = False

    is_mkt = fields.Boolean(string="check mkt", compute="is_mkt_act")
    is_pde_check = fields.Boolean(string="check pde", compute='is_pde')

    @api.one
    def is_mkt_act(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('sales_team.group_sale_salesman'):
            self.is_mkt = True

        else:
            self.is_mkt = False

    # State untuk PDE button (Confirm dan Reset To Previous)
    @api.one
    def is_pde(self):
        state = int(self.state)
        if state == 7:
            self.is_pde_check = True
        elif state == 3:
            self.is_pde_check = True
        elif state == 1:
            self.is_pde_check = True


    x_price_low = fields.Float('Price Low', digits=dp.get_precision('Prroduct Price'))
    x_price_high = fields.Float('Price High', readonly=True, digits=dp.get_precision('Prroduct Price'))
    x_hpp = fields.Float('HPP', readonly=True, digits=dp.get_precision('Prroduct Price'))

    x_length_m = fields.Float(readonly=True, store=True,states={'1': [('readonly', False)]},
                              digits=dp.get_precision('Payment Terms'))
    x_width_m = fields.Float(readonly=True, store=True, states={'1': [('readonly', False)]},
                             digits=dp.get_precision('Payment Terms'))

    # DataForm
    x_length_prd = fields.Float(related="x_product.x_length")
    x_width_prd = fields.Float(related="x_product.x_width")
    x_ink_coverage_pde_prd = fields.One2many(related="x_product.x_ink_coverage_pde")
    x_special_color_prd = fields.Boolean(related="x_product.x_special_color")
    x_diecut_shape_id_prd = fields.Many2one(related="x_product.x_diecut_shape_id")
    x_material_type_ids_prd = fields.One2many(related="x_product.x_material_type_ids")
    x_release_prd = fields.Many2one(related="x_product.x_release")
    x_hotprint_list_ids_prd = fields.One2many(related="x_product.x_hotprint_list_ids")
    x_finishing_process_laminating_prd = fields.Many2one(related="x_product.x_finishing_process_laminating")
    x_finishing_process_emboss_prd = fields.Many2one(related="x_product.x_finishing_process_emboss")
    # x_finishing_process_foil_prd = fields.Many2one(related="x_product.x_finishing_process_foil")
    x_media_tempel_prd = fields.Char(related="x_product.x_media_tempel")
    x_location_media_id_prd = fields.One2many(related="x_product.x_location_media_id")
    x_varnish_list_ids_prd = fields.One2many(related="x_product.x_varnish_list_ids")
    x_layout_product_ids_prd = fields.One2many(related="x_product.x_layout_product_ids")
    x_active_prd = fields.Boolean(related="x_product.active")
    x_drawing_prd = fields.Many2one(related="x_product.x_drawing")
    x_drawing_file_prd = fields.Binary(related="x_product.x_drawing_file")
    x_categ_id_prd = fields.Many2one(related='x_product.categ_id', string="Category Product")
    # x_gramature_prd = fields.Float(related='x_product.')

    # ribbon spech
    x_ribbon_prd = fields.Many2one(related="x_product.x_ribbon")
    x_face_ink_prd = fields.Selection(related="x_product.x_face_ink")
    x_id_core_prd = fields.Float(related="x_product.x_id_core")
    # x_id_core_m = fields.Float('ID Core')
    x_od_core_prd = fields.Float(related="x_product.x_od_core")
    # x_od_core_m = fields.Float('OD Core')
    x_core_type_prd = fields.Selection(related="x_product.x_core_type")
    x_notch_prd = fields.Boolean(related="x_product.x_notch")
    x_roll_perbox_ribbon_prd = fields.Integer(related="x_product.x_roll_perbox_ribbon")
    x_material_core_prd = fields.Selection(related="x_product.x_material_core")

    @api.onchange("x_length", "x_width")
    def check_konversi(self):
        if self.x_length > 0:
            self.x_length_m = self.x_length / 1000
        if self.x_width > 0:
            self.x_width_m = self.x_width / 1000

    @api.onchange("x_repeat_order")
    def check_repeat(self):
        if self.x_repeat_order == True:
            self.x_repeat_order = True

    @api.onchange("x_status_cr")
    def check_repeat_a(self):
        if self.x_status_cr == 'reject':
            self.state = '9'

    @api.multi
    def action_next(self):
        if self.x_repeat_order == True:
            new_state = int(self.state)
        else:
            new_state = int(self.state) + 1

        self.state = str(new_state)
        self.color = 3

    @api.multi
    def action_prev(self):
        new_state = int(self.state) - 1
        self.state = str(new_state)
        self.color = 3

    @api.multi
    def action_draft(self):
        self.state = '1'

    @api.multi
    def action_confirm(self):
        self.state = '2'

    @api.multi
    def action_done(self):
        self.state = '3'

    @api.multi
    def write(self, vals):

        if self.x_repeat_order == True:
            vals['state'] = '9'

        insert_obj = self.env['x.approvalstage'].create({'name': self.name, 'description': self.state})

        return super(prod_requirement, self).write(vals)

    @api.model
    def create(self, vals):

        if vals['x_repeat_order'] == True:
            vals['state'] = '9'
        else:
            vals['state'] = '1'

        vals['name'] = self.env['ir.sequence'].next_by_code('x.cusrequirement') or _('New')
        result = super(prod_requirement, self).create(vals)

        return result

    @api.onchange('x_product')
    def repeat_price(self):
        for a in self.x_sale_order_line_ids:
            self.x_id = a.product_id
        self.env.cr.execute("SELECT max(id) FROM sale_order_line where product_id = " + str(self.x_id))
        self.x_tamp_tgl = self.env.cr.fetchone()[0]
        for x in self.x_sale_order_line_ids:
            if x.id == self.x_tamp_tgl:
                self.x_harga_repeat = x.price_unit

    @api.onchange('x_cusreq', 'x_repeat_order')
    def repeat_spec(self):
        if self.x_repeat_order == True:
            self.x_length = self.x_cusreq.x_length
            self.x_width = self.x_cusreq.x_width
            self.x_packing_category_id = self.x_cusreq.x_packing_category_id
            self.x_supplier_id = self.x_cusreq.x_supplier_id
            self.x_material_type_id = self.x_cusreq.x_material_type_id
            self.x_numbers_of_colors = self.x_cusreq.x_numbers_of_colors
            self.x_varnish = self.x_cusreq.x_varnish
            self.x_special_color = self.x_cusreq.x_special_color
            self.x_ink_coverage = self.x_cusreq.x_ink_coverage
            self.x_mrpwordkcenter_id = self.x_cusreq.x_mrpwordkcenter_id
            self.x_lamination = self.x_cusreq.x_lamination
            self.x_category_foil = self.x_cusreq.x_category_foil

    @api.multi
    def act_reject(self):
        self.x_status_cr = 'reject'
        self.state = '9'


class approval_stage(models.Model):
    _name = 'x.approvalstage'
    name = fields.Char()
    description = fields.Text()


#
class product_sales(models.Model):
    _inherit = 'product.product'
    x_product_sol = fields.One2many('sale.order.line', 'product_id', string='product sale order line')
    # x_prod_cusreq = fields.One2many('x.cusrequirement', 'x_cusreq', string = 'Customer Requirement')

class x_konv_material(models.Model):
    _name = 'x.konversi.material'
    name = fields.Char(string = 'KM_Odoo')
    x_km_precost = fields.Char(string='KM_Precost')

