# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp
from datetime import datetime
from dateutil.relativedelta import relativedelta


class prod_requirement(models.Model):
    _name = 'x.cusrequirement'  #akan dipake untuk CR
    _inherit = 'mail.thread'

    name = fields.Char(string='Code')
    x_sq = fields.Many2one('x.sales.quotation', string = 'Sales Quotation')
    x_sq_prod = fields.Many2one('product.product')

    x_duedate_drawing = fields.Datetime(string='Due Date Drawing',readonly = True ) #default=datetime.now()
    item_description = fields.Char(string='Item Name', readonly=True,

                                   # states={'1': [('readonly', False)]}, *Dwi
                                   track_visibility='always')
    description = fields.Text(track_visibility='onchange', readonly = True) #dwi tambah readonly = True

    color = fields.Integer('Warna')
    state = fields.Selection(
        [('0', 'Marketing'), ('1', 'Drawing'), ('2', 'Approval Cus (Drawing)'), ('3', 'Drawing Approved'), ('4', 'PDE (Tech. Spec) '),
         ('5', 'Digital Proof'),
         ('6', 'Trial Product'), ('7', 'Approval Trial'), ('8', 'Finalize TDS'), ('9', 'Done'), ('cancel', 'Cancel')
         ], default='0', track_visibility='onchange', string="Status Product")

    x_product = fields.Many2one('product.product', string='Product Name', related = 'x_sq.x_product', domain=[('sale_ok', '=', True)])
    x_locked_product = fields.Boolean(related='x_product.x_locked_ok', string="Locked Product", readonly=True, store=True)
    x_product_tmpl = fields.Many2one('product.template', string='Product Template', domain=[('sale_ok', '=', True)])
    x_quotation_id = fields.Many2one('sale.order')
    # x_sale_order_line_ids = fields.One2many('sale.order.line', related='x_product.x_product_sol', readonly=True)
    # x_cusreq = fields.Many2one(string = 'name last SQ', related = 'x_sale_order_line_ids.x_customer_requirement')
    x_no_so = fields.Char(string='No. SO')
    x_harga_repeat = fields.Float(readonly=True, string='Harga Repeat')
    x_tamp_tgl = fields.Integer(string='tampungan tanggal untuk loop', readonly=True)
    x_id = fields.Integer(string='tampungan tanggal untuk loop', readonly=True)
    x_request_date = fields.Date(string='Request Date',store=True, readonly = True, default=fields.Datetime.now)
    x_print = fields.Boolean(string = 'print', readonly = False)

    # TIMESHEET PDE
    x_timetracking_dr = fields.One2many('x.timetracking.drawing','x_cus')
    x_estimated_duration = fields.Float(string='Estimated Duration (hour)')
    x_duedate_startdrawing = fields.Datetime(string='Duedate Start', default = datetime.now())
    x_estimatedfinish_drawing = fields.Datetime(string='Estimated Finish Drawing')
    x_staff_drawing = fields.Many2one('res.partner',string='Staff Drawing')

    @api.multi
    def btn_sq(self):
        self.item_description = self.x_sq.item_description
        self.x_repeat_order = self.x_sq.x_repeat_order
        self.description = self.x_sq.description
        self.x_sales_id = self.x_sq.x_sales_id
        self.x_customer_id = self.x_sq.x_customer_id
        self.x_qty = self.x_sq.x_qty
        self.x_satuan = self.x_sq.x_satuan
        # self.x_material_number = self.x_sq.x_material_number
        self.x_length = self.x_sq.x_length
        self.x_width = self.x_sq.x_width
        self.x_packing_category_id = self.x_sq.x_packing_category_id
        self.x_mrpwordkcenter_id = self.x_sq.x_mrpwordkcenter_id
        self.x_lamination = self.x_sq.x_lamination
        self.x_category_foil = self.x_sq.x_category_foil
        self.x_supplier_id = self.x_sq.x_supplier_id
        self.x_material_type_id = self.x_sq.x_material_type_id
        self.x_numbers_of_colors = self.x_sq.x_numbers_of_colors
        self.x_varnish = self.x_sq.x_varnish
        self.x_special_color = self.x_sq.x_special_color
        self.x_ink_coverage = self.x_sq.x_ink_coverage
        self.x_reg_cr_mkt = self.x_sq.x_reg_cr_mkt
        self.x_jumlah_cr_mkt = self.x_sq.x_jumlah_cr_mkt

    @api.onchange('x_estimated_duration')
    def estimated_drawing(self):
        if self.x_duedate_startdrawing:
            format = "%Y-%m-%d %H:%M:%S"
            date_var = datetime.strptime(str(self.x_duedate_startdrawing), format)
            self.x_estimatedfinish_drawing = date_var + relativedelta(hours=float(self.x_estimated_duration))

        # self._update_reg_cr(self)

    @api.multi
    def set_calendar(self):

        calendar_event = self.env['calendar.event']
        calendar_event.create({
                'name': str(self.item_description) + " for " + str(self.x_customer_id.name),
                'partner_ids': [(4,self.x_staff_drawing.id)],
                'start_datetime': self.x_duedate_startdrawing,
                'start': self.x_duedate_startdrawing,
                'stop': self.x_estimatedfinish_drawing,
                'alarm_ids': [(4, 1)],
                #     # 'company_id': self.company_id.id,
            })


    # @api.onchange('x_duedate_startdrawing')
    # def datestartdrawing_calendar(self):
    #     calendar_event = self.env['calendar.event']
    #     calendar_event.create({
    #         'name': 'satu dua',
    #         'partner_ids': [(4,6)],
    #         'start_datetime': self.x_duedate_startdrawing,
    #         'start': self.x_duedate_startdrawing,
    #         'stop': self.x_duedate_startdrawing,
    #         'alarm_ids': [(4, 1)],
    #         #     # 'company_id': self.company_id.id,
    #     })

    # Pre-Costing
    x_category_foil = fields.Many2one('x.category.finishing.process', string='Category Foil', readonly=True) #*dwi hapus ini , states={'1': [('readonly', False)]}
    x_customer_id = fields.Many2one('res.partner', string='Customer', domain=[('customer', '=', True)], readonly=True) #*dwi hapus ini , states={'1': [('readonly', False)]}

    x_ink_coverage = fields.Selection([('0.0', '0.0'), ('0.25', '0.25'), ('0.5', '0.5'), ('0.75', '0.75'), ('1', '1')], readonly=True, string='Ink Coverage') #*dwi hapus ini , states={'1': [('readonly', False)]}
    x_lamination = fields.Boolean('Lamination', readonly=True) #*dwi hapus ini , states={'1': [('readonly', False)]}
    x_length = fields.Float('Length (mm)', readonly=True) #*dwi hapus ini , states={'1': [('readonly', False)]}
    x_material_number = fields.Char('Material Number', readonly=True) #*dwi hapus ini , states={'1': [('readonly', False)]}
    x_material_type_id = fields.Many2one('product.template', 'Material Type', readonly=True) #*dwi hapus ini ,states={'1': [('readonly', False)]}, domain=[('categ_id.sts_bhn_utama.name', '=', 'Bahan Utama')]
    x_mrpwordkcenter_id = fields.Many2one('mrp.workcenter', 'Prime Machine', readonly=True) #*dwi hapus ini ,states={'1': [('readonly', False)]}
    x_name = fields.Char('Product Name', readonly=True, states={'1': [('readonly', False)]})
    x_numbers_of_colors = fields.Integer('Number Of Color', readonly=True) #*dwi hapus ini , states={'1': [('readonly', False)]}
    x_packing_category_id = fields.Many2one('x.packing.category', 'Packing Category', readonly=True) #*dwi hapus ini ,states={'1': [('readonly', False)]}
    x_qty = fields.Integer('Qty (pcs)', readonly=True) #*dwi hapus ini , states={'1': [('readonly', False)]}
    x_sales_id = fields.Many2one('res.partner', string='Sales',
                                 domain=[('customer', '=', False), ('supplier', '=', False)], readonly=True) #*dwi hapus ini ,states={'1': [('readonly', False)]}
    x_special_color = fields.Boolean('Special Color', readonly=True)#*dwi hapus ini , states={'1': [('readonly', False)]}
    x_supplier_id = fields.Many2one('res.partner', string='Suplier', domain=[('supplier', '=', True)], readonly=True) #*dwi hapus ini ,states={'1': [('readonly', False)]}
    x_varnish = fields.Boolean('Varnish', readonly=True) #*dwi hapus ini , states={'1': [('readonly', False)]}
    x_width = fields.Float('Width (mm)', readonly=True) #*dwi hapus ini , states={'1': [('readonly', False)]}

    x_repeat_order = fields.Boolean('Repeat Order', readonly = True) #*dwi tambah readonly = True
    x_status_cr = fields.Selection(
        [('draft', 'Draft'), ('SPV', 'Need Approval SPV'), ('approve', 'Approve'), ('done', 'Done'),
         ('reject', 'Reject')],
        default='draft', string='Status SQ', readonly = True, related = 'x_sq.x_status_cr')

    x_satuan = fields.Selection([('sheet', 'Sheet'), ('roll', 'Roll'), ('fanfold', 'Fan Fold')], string='Satuan',
                                Default='sheet', readonly=True) #*dwi hapus ini ,states={'1': [('readonly', False)]}

    x_propose_price_low = fields.Float('Porpose Price Low', readonly=True, digits=dp.get_precision('Prroduct Price'))
    x_propose_price_high = fields.Float('Porpose Price High', readonly=True, digits=dp.get_precision('Prroduct Price'))
    x_propose_profit_low = fields.Float('Porpose Profit Low', readonly=True, digits=dp.get_precision('Prroduct Price'))
    x_propose_profit_high = fields.Float('Porpose Profit High', readonly=True,
                                         digits=dp.get_precision('Prroduct Price'))
    compute_field = fields.Boolean(string="check field", compute = "get_user")
    x_is_salemanager = fields.Boolean(string="check field apakah sales manager", compute = "cek_sales_manager")
    start_of_date = fields.Date(string='Price Start Date', readonly=True)
    end_of_date = fields.Date(string="Price End Date", compute='end_date_function')

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

    is_mkt = fields.Boolean(string="check mkt", compute="is_mkt_act")
    is_pde_check = fields.Boolean(string="check pde", compute='is_pde')

    # uswa tambah ini
    is_pde_user = fields.Boolean(string="check pde", compute='is_pde_act')

    @api.one
    def is_mkt_act(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('sales_team.group_sale_salesman'):
            self.is_mkt = True
        else:
            self.is_mkt = False

    @api.one
    def is_pde_act(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('lpj_product.group_pde_user'):
            self.is_pde_user = True

        else:
            self.is_pde_user = False



    # State untuk PDE button (Confirm dan Reset To Previous)
    @api.one
    def is_pde(self):
        if self.state == 'cancel':
            pass
        # uswa-tambah ini
        # elif (fafiru?)
        #     self.is_mkt = True
        else:
            state = int(self.state)
            if state == 7:
                self.is_pde_check = True
            elif state == 3:
                self.is_pde_check = True
            elif state == 2:
                self.is_pde_check = True
            elif state == 0:
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

    # Color Range
    x_reg_cr_mkt = fields.Boolean('Request Color Range', readonly = True)
    x_jumlah_cr_mkt = fields.Integer('Request Color Range Count', readonly = True)

    x_reg_cr_pde = fields.Boolean('Request Color Range', related="x_product.x_reg_cr_pde_m")
    x_jumlah_cr_pde = fields.Integer('Request Color Range Count', related="x_product.x_jumlah_cr_pde_m")

    # @api.onchange('state')
    # def _notif_proof(self):
    #     self.x_length_prd = 1234
        # # if self.state == '3':
        #     template = self.env.ref('lpj_cusrequire.template_mail_proof')
        #     mail = self.env['mail.template'].browse(template.id)
        #     mail.send_mail(self.x_sales_id, force_send=True)  # langsung kirim email


    # Trigger untuk update field di master product
    @api.onchange('x_jumlah_cr_mkt','x_reg_cr_mkt','x_repeat_order','x_product')
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



    @api.onchange("x_length", "x_width")
    def check_konversi(self):
        if self.x_length > 0:
            self.x_length_m = self.x_length / 1000
        if self.x_width > 0:
            self.x_width_m = self.x_width / 1000


    @api.onchange("x_repeat_order")
    def check_repeat(self):
        if self.x_repeat_order == True:
            if self.x_product:
                self.env.cr.execute("select x_material_type_id, x_length, x_width, x_varnish, x_special_color,"
                                    " x_ink_coverage, x_mrpwordkcenter_id, x_lamination, x_category_foil from x_cusrequirement where "
                                    "x_product = '" + str(self.x_product.id) + "'and create_date = (select max(create_date) from x_cusrequirement where x_product = '" + str(self.x_product.id) +"')")
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
        # self.x_length_prd = 1234
        if self.state == '2':
            template = self.env.ref('lpj_cusrequire.template_mail_proof')
            mail = self.env['mail.template'].browse(template.id)
            mail.send_mail(self.id, force_send=True)  # langsung kirim email

    @api.multi
    def action_prev(self):
        new_state = int(self.state) - 1
        self.state = str(new_state)
        self.color = 2

    @api.multi
    def action_draft(self):
        self.state = '0'

    @api.multi
    def action_confirm(self):
        self.state = '1'

    @api.multi
    def action_done(self):
        self.state = '2'

    @api.multi
    def write(self, vals):

        if self.x_repeat_order == True:
            vals['state'] = '9'

        insert_obj = self.env['x.approvalstage'].create({'name': self.name, 'description': self.state})

        return super(prod_requirement, self).write(vals)

    @api.model
    def create(self, vals):
        #*dwi
        # if vals['x_repeat_order'] == True:
        #     vals['state'] = '9'
        # else:
        #     vals['state'] = '1'

        vals['name'] = self.env['ir.sequence'].next_by_code('x.cusrequirement') or _('New')

        result = super(prod_requirement, self).create(vals)
        # Tanggal start date otomatis ambil hari ini
        result.write({'start_of_date': datetime.now()})
        # self._update_reg_cr(self)

        return result

    @api.multi
    def act_approve(self):
        self.x_status_cr = 'approve'

    @api.multi
    def act_reject(self):
        self.x_status_cr = 'reject'
        self.state = '10'
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

    # Function untuk button digital proof langsung ke approval trial
    @api.multi
    def action_approval_trial(self):
        self.state = '8'

    # Fungsi menambah end date + 60 hari
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

    # Action button create drawing
    @api.multi
    def btn_drawing(self):
        for cusreq in self:
            view = cusreq.env['ir.model.data'].xmlid_to_res_id('lpj_product.drawing_form_view', raise_if_not_found=True)

            customer = cusreq.x_customer_id.id
            item_name = cusreq.item_description

            result = {
                'name': 'Create Drawing',
                'view_type': 'form',
                'res_model': 'x.drawing',
                'view_id': view,
                'context': {
                    'default_x_partner': customer,
                    'default_x_description': item_name
                },
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'target': 'new'
            }
            return result

    @api.multi
    def action_cancel(self):
        self.state = 'cancel'

class approval_stage(models.Model):
    _name = 'x.approvalstage'

    name = fields.Char()
    description = fields.Text()


class x_konv_material(models.Model):
    _name = 'x.konversi.material'

    name = fields.Char(string = 'KM_Odoo')
    x_km_precost = fields.Char(string='KM_Precost')

class reject_reason(models.Model):
    _name = 'x.reject.reason'

    name = fields.Char(string = 'SQ', readonly = True)
    x_reject_reason = fields.Many2one('x.master.reason',string='Reason')
    x_desc = fields.Text(string='Description')

class reject(models.Model):
    _name = 'x.master.reason'

    name = fields.Text(string='Reason')

class time_track_drawing(models.Model):
    _name = 'x.timetracking.drawing'

    x_cus = fields.Many2one('x.cusrequirement', string = 'Kode Drawing Request')
    x_tglstart = fields.Datetime(string = 'Start Date', readonly = True)
    x_tglend = fields.Datetime(string = 'End Date', readonly = True)
    x_duration = fields.Float(string = 'Duration (hour:minutes)', readonly = True)
    x_category_drawing = fields.Selection(
        [('ldfa', 'Layout & DFA'), ('simple_redraw', 'Simple Redraw'), ('full_redraw', 'Full Redraw')], default='ldfa',string="Category Drawing")
    x_user = fields.Many2one('res.users', 'User', readonly=True, default=lambda self: self.env.user)
    x_desc = fields.Text(string = 'Keterangan')


    @api.multi
    def start_dr_duration(self):
        self.x_tglstart = datetime.now()

    @api.multi
    def stop_dr_duration(self):
        self.x_tglend = datetime.now()
        time_diff = fields.Datetime.from_string(self.x_tglend) - fields.Datetime.from_string(self.x_tglstart)
        self.x_duration = float(time_diff.days) * 24 + (float(time_diff.seconds) / 3600)
        # fmt = '%Y-%m-%d %H:%M:%S'
        # sd= datetime.strptime(self.x_tglstart,fmt)
        # se = datetime.strptime(self.x_tglend, fmt)
        # self.x_duration = (se-sd).days * 24 * 60
        # start_dt = fields.Datetime.from_string(self.x_tglstart)
        # finish_dt = fields.Datetime.from_string(self.x_tglend)
        # difference = relativedelta(finish_dt, start_dt)
        # self.x_duration = difference.hours