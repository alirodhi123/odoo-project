# -*- coding: utf-8 -*-
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api

import base64
import odoo.addons.decimal_precision as dp



class print_quotation_line(models.Model):
    _name = 'x.print.quo.line'
    _inherit = 'mail.thread'

    x_quo = fields.Many2one('x.print.quo', string = 'cusreq quotation',track_visibility='always', ondelete='cascade')
    x_sq = fields.Many2one('x.sales.quotation',string = 'Sales Quotation Code', track_visibility='always')
    x_item_desc = fields.Char(related = 'x_sq.item_description', track_visibility='onchange')
    x_prod = fields.Many2one(related = 'x_sq.x_product', readonly = True)
    x_qty = fields.Integer(string = 'Quantity', track_visibility='onchange', related = 'x_sq.x_qty', readonly = True)
    x_width= fields.Float(string='Width', track_visibility='onchange', related='x_sq.x_width', readonly=True)
    x_length = fields.Float(string='Length', track_visibility='onchange', related='x_sq.x_length', readonly=True)
    x_material_type_id = fields.Many2one('product.template', 'Material Type',related='x_sq.x_material_type_id',readonly=True)
    x_flag = fields.Boolean(related = 'x_sq.x_flag_quo')
    x_price_pcs = fields.Float(string = 'Harga Pcs',readonly = True, track_visibility='always', related = 'x_sq.x_price_fix')
    x_total_price = fields.Float(string = 'Total Harga',  readonly = True)
    currency_id = fields.Many2one("res.currency", related='x_quo.currency_id', string="Currency", readonly=True,required=True)
    x_manufacturing_type = fields.Selection([('laprint', 'Laprint'), ('digital', 'Digital')],
                                            default='laprint', string='Manufacturing Type',
                                            related='x_sq.x_manufacturing_type', readonly=True,
                                            track_visibility='onchange', required=True)
    x_planning_type = fields.Selection([('forward', 'Forward Planning'), ('backward', 'Backward Planning')],
                                       default='forward', string='Planning Type',
                                       related='x_sq.x_planning_type', readonly=True,
                                       track_visibility='onchange', required=True)
    x_finishing = fields.Char(string = 'Finishing', store = True)
    x_price_pcs_ppn = fields.Float(string='Harga Pcs include ppn', readonly=True, track_visibility='always', compute='price_ppn')
    x_bahan = fields.Char(string='Material Type', readonly=True, track_visibility='always',
                                   compute='price_ppn')


    @api.multi
    def price_ppn(self):
        for row in self:
            row.x_price_pcs_ppn = float(row.x_price_pcs*0.1)+float(row.x_price_pcs)
            id_bahan = row.x_material_type_id.id
            bahan = row.env['product.template'].search([('id', '=', id_bahan)])
            if bahan:
                for bhn in bahan:
                    row.x_bahan = bhn.name[6:]



    @api.onchange('x_sq')
    def finishing(self):
        x_varn = self.x_sq.x_varnish
        x_special = self.x_sq.x_special_color
        x_lamin = self.x_sq.x_lamination
        x_foil = self.x_sq.x_category_foil.id
        name_foil = self.env['x.category.finishing.process'].search([('id', '=', x_foil)])
        if name_foil:
            for x in name_foil:
                nama_f = x.name
                if nama_f == 'None':
                    nama_foil = 'No'
                elif nama_f == 'none':
                    nama_foil = 'No'
                elif nama_f == 'Half':
                    nama_foil = 'Half'
                else:
                    nama_foil = 'Full'

            if x_varn == True:
                self.x_finishing = nama_foil + ' Foil + ' + 'Varnish'
                if x_special == True:
                    self.x_finishing = nama_foil + ' Foil + ' + 'Varnish + Special Color'
                    if x_lamin == True:
                        self.x_finishing = nama_foil + ' Foil + ' + 'Varnish + Special Color + Laminating'
                    else:
                        self.x_finishing = nama_foil + ' Foil + ' + 'Varnish + Special Color'
                else:
                    if x_lamin == True:
                        self.x_finishing = nama_foil + ' Foil + ' + 'Varnish + Laminating'
                    else:
                        self.x_finishing = nama_foil + ' Foil + ' + 'Varnish'
            else:
                if x_special == True:
                    self.x_finishing = nama_foil + ' Foil + ' + 'Special Color'
                    if x_lamin == True:
                        self.x_finishing = nama_foil + ' Foil + ' + 'Special Color + Laminating'
                    else:
                        self.x_finishing = nama_foil + ' Foil + ' + 'Special Color'
                else:
                    if x_lamin == True:
                        self.x_finishing = nama_foil + ' Foil + ' + 'Laminating'
                    else:
                        self.x_finishing = nama_foil + ' Foil'

        else:
            if x_varn == True:
                self.x_finishing = 'Varnish'
                if x_special == True:
                    self.x_finishing = 'Varnish + Special Color'
                    if x_lamin == True:
                        self.x_finishing = 'Varnish + Special Color + Laminating'
                    else:
                        self.x_finishing = 'Varnish + Special Color'
                else:
                    if x_lamin == True:
                        self.x_finishing = 'Varnish + Laminating'
                    else:
                        self.x_finishing = 'Varnish'
            else:
                if x_special == True:
                    self.x_finishing = 'Special Color'
                    if x_lamin == True:
                        self.x_finishing = 'Special Color + Laminating'
                    else:
                        self.x_finishing = 'Special Color'
                else:
                    if x_lamin == True:
                        self.x_finishing = 'Laminating'
                    else:
                        self.x_finishing = 'None'

    @api.model
    def create(self, vals):
        vals['x_flag'] = True
        result = super(print_quotation_line, self).create(vals)
        return result


    @api.onchange('x_price_pcs','x_qty')
    def harga(self):
        self.x_qty = self.x_sq.x_qty
        self.x_total_price = self.x_price_pcs * self.x_qty

class print_quotation(models.Model):
    _name = 'x.print.quo'
    _inherit = 'mail.thread'

    name = fields.Char(string = 'Quotation', track_visibility='always')
    x_cust = fields.Many2one('res.partner', string = 'Customer')
    x_quo_line = fields.One2many('x.print.quo.line', 'x_quo', required=True, track_visibility='always')
    x_cusreq_quo = fields.Many2one(related = 'x_quo_line.x_sq')
    x_untaxed_amount = fields.Float(string='Total Harga',compute = 'total_harga' ,readonly=True, track_visibility='always')
    currency_id = fields.Many2one('res.currency')
    is_responsible = fields.Boolean(default=False, string="SPH Closed")
    start_date = fields.Date(string="Start Date", store=True, readonly=True)
    end_date_value = fields.Date(string="End Date SQ", compute='end_date_function')
    x_pic_cust = fields.Char(string = 'PIC Customer')
    x_jenis_sph = fields.Selection(
        [('penawaran', 'Penawaran'), ('negosiasi', 'Negosiasi')],
        default='penawaran', string='Jenis SPH')
    x_payment_term = fields.Many2one('account.payment.term', string= 'Payment Term')
    x_user_id = fields.Many2one('res.users', string='Admin')
    x_note = fields.Text('Note')

    @api.onchange("x_cust")
    def check_repeat(self):
        self.x_user_id = self.x_cust.user_id.id
        id_partner1 = self.x_cust.id
        id_partner = 'res.partner,' + str(id_partner1)
        ir_property = self.env['ir.property'].search([('res_id', '=', id_partner), ('name', '=', 'property_payment_term_id')])
        if ir_property:
            for x in ir_property:
                payment_term = x.value_reference.strip('account.payment.term,')
                self.x_payment_term = int(payment_term)
    @api.one
    def total_harga(self):
        ab = 0
        for a in self.x_quo_line:
            a.x_total_price = a.x_price_pcs * a.x_qty
            ab += a.x_total_price
        self.x_untaxed_amount = ab


    @api.model
    def create(self, vals):
        result = super(print_quotation, self).create(vals)

        sequence = self.env['ir.sequence'].next_by_code('x.print.quo') or ('New')
        result.write({'name': sequence})

        result.write({'start_date': datetime.now()})

        return result


    # Fungsi menambah end date + 60 hari
    @api.one
    def end_date_function(self):
        # Menambah end of date + 60 hari
        end_date = self.start_date

        if end_date != False:

            jumlah_hari = '90'
            date_format = '%Y-%m-%d'
            date = self.start_date

            start_date_var = datetime.strptime(str(date), date_format)
            end_date_var = start_date_var + relativedelta(days=int(jumlah_hari))
            self.end_date_value = str(end_date_var)

    def x_send_quotation(self):
        '''
                This function opens a window to compose an email, with the edi sale template message loaded by default
                '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('lpj_cusrequire', 'mail_template_sph')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict()
        ctx.update({
            'default_model': 'x.print.quo',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "lpj_cusrequire.mail_template_data_notification_email_sph"
        })
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
        # self.ensure_one()
        # attachment = {
        #     'name': ("%s" % self.filename),
        #     'datas': self.get_file_data(),
        #     'datas_fname': self.filename,
        #     'res_model': 'x.print.quo',
        #     'type': 'binary'
        # }
        # id = self.env['ir.attachment'].create(attachment)
        # email_template = self.env.ref('my.email_template_example')
        # email_template.attachment_ids = False
        # email_template.attachment_ids = [(4, id.id)]
        #
        # ir_model_data = self.env['ir.model.data']
        # try:
        #     template_id = ir_model_data.get_object_reference('my', 'email_template_example')[1]
        # except ValueError:
        #     template_id = False
        # try:
        #     compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        # except ValueError:
        #     compose_form_id = False
        # ctx = dict()
        # ctx.update({
        #     'default_model': 'x.print.quo',
        #     'default_res_id': self.ids[0],
        #     'default_use_template': bool(template_id),
        #     'default_template_id': template_id,
        #     'default_composition_mode': 'comment',
        #     'attachment_ids': [(4, id.id)],
        # })
        # return {
        #     'type': 'ir.actions.act_window',
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'mail.compose.message',
        #     'views': [(compose_form_id, 'form')],
        #     'view_id': compose_form_id,
        #     'target': 'new',
        #     'context': ctx,
        # }


        # CREATE ATTACHMENT OTOMATIS
        # pdf = self.env['report'].sudo().get_pdf([self.id], 'lpj_cusrequire.report_document_quo')
        # self.env['ir.attachment'].create({
        #     'name': 'Cats',
        #     'type': 'binary',
        #     'datas': base64.encodestring(pdf),
        #     'res_model': 'x.print.quo',
        #     'res_id': self.id,
        #     'mimetype': 'application/x-pdf'
        # })


class flag_quo(models.Model):
    _inherit = 'x.sales.quotation'

    x_flag_quo = fields.Boolean(string ='Internal Quotation', default = False)
    x_internal_code = fields.Char(string = 'Internal Code')
    x_quo_line_id = fields.One2many('x.print.quo.line','x_sq', string = 'Print Quo Line')
    x_quo_parent = fields.Many2one('x.print.quo', related = 'x_quo_line_id.x_quo')


