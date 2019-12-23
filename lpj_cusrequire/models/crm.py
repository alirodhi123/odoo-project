# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, time
import odoo.addons.decimal_precision as dp
# from . import crm_stage

class x_crm_stage(models.Model):
    _inherit = 'crm.stage'
    _order = "x_order"

    x_order = fields.Integer(string = 'Stage Order')



class x_crm(models.Model):
    _inherit = 'crm.lead'

    x_flag_sq = fields.Boolean(default = False)
    x_type_company = fields.Char(string = 'Company Type')
    x_estimated_product = fields.One2many('x.estimated.product.crm','x_crm_lead')
    x_is_qualified = fields.Boolean(string = 'status qualified', default = True)
    x_status_job = fields.Selection([('repeat', 'Repeat'), ('new', 'New')], string='Status Job')
    x_cs_lead = fields.Many2one('res.users',string = 'Customer Services')
    x_partner = fields.Many2one('res.partner', related = 'partner_id')
    x_status_lead = fields.Many2one('x.lead.status', string='Lead Status', required=True)
    x_source_lead = fields.Many2one('x.lead.source', string='Lead Source', required=True)

    # @api.onchange('stage_id')
    # def status_customer(self):
    #     self.partner_id.x_status_cust = "ABC"
    #     # self.env.cr.execute("select pipeline_customer ('" + str(self.partner_id.id) + "')")

    @api.multi
    def is_qualified(self):
        return self.write({'x_is_qualified': False})
        # self.x_is_qualified = 'f'
        # false = tidak qualified


class x_mail_message(models.Model):
    _inherit = 'mail.message'

    x_partner = fields.Many2one('res.partner',string='Partner')
    x_type_activity = fields.Char('Activity Type', store=True)
    x_lead_jobpotential = fields.Many2one('crm.lead', string = 'job potential')
    x_PIC = fields.Many2one('res.users', string = 'PIC action')
    x_contact = fields.Char( string='PIC yang ditemui')
    x_contact_dept = fields.Char(string='Dept pic ditemui')
    x_contact_phone = fields.Char(string='Contact yang ditemui')
    # x_datecreate_nextact = fields.Date(string='Date created next activity (as actual date execute last activity)', default = datetime.now())
    x_next_activity = fields.Many2one('crm.activity', string = 'next activity in mail message')
    x_execute_activity = fields.Date(string='Execution date')
    # x_recommended_act = fields.Many2one('crm.activity', string='recommended activity id')
    # x_summary_nextact = fields.Char(string='Summary Next Activity')


class x_partner(models.Model):
    _inherit = 'res.partner'


    x_mail_message = fields.One2many('mail.message', 'x_partner', string='Mail Message')
    x_partnernext_activity_id = fields.Many2one('crm.activity', 'Activity', store = True)
    x_partnertitle_action = fields.Char('Summary', store = True)
    x_partnernote = fields.Html('Note', store = True)
    x_partnerdate_deadline = fields.Datetime('Expected Closing', store = True)
    x_partnerplanned_revenue = fields.Float('Expected Revenue', store = True)
    x_PIC_action = fields.Many2one('res.users', store=True)
    x_lead = fields.One2many('crm.lead', 'partner_id')
    x_stage_lead = fields.Many2one('crm.stage', related = 'x_lead.stage_id')
    x_pipeline_customer = fields.Char(string='Pipeline Customer tampungan')
    x_status_cust_ids = fields.Char(compute='status_customer_crm', readonly = True)
    # x_sementara = fields.Char(string='Pipeline Customer', readonly = True)
    # x_status_cuts_id = fields.Char(string='Customer Pipeline')

        # # self.x_pipeline_customer = 'AAAAA'
        # # self.x_status_cust = self.name
        # self.env.cr.execute("select pipeline_customer ('"+ str(self.id) +"')")
        # # self.env.cr.execute("select distinct (cs.name) from crm_lead cl "
        # #                         "left join res_partner rp on cl.partner_id = rp.id "
        # #                         "left join crm_stage cs on cl.stage_id = cs.id "
        # #                         "where cl.stage_id = (select max(stage_id) from crm_lead where x_order not in (2000,2001) and partner_id =" + str(self.id) + ")")
        # cus = self.env.cr.fetchone()
        # if cus:
        #     self.x_pipeline_customer = cus[0]

    @api.multi
    def action_log_res(self):
        for log in self:
            log.x_lead.write({
                'title_action': log.x_partnertitle_action,
                'date_action': log.x_partnerdate_deadline,
                'next_activity_id': log.x_partnernext_activity_id.id,
            })
            body_html = "<div><b>%(title)s</b>: %(next_activity)s</div>%(description)s%(note)s" % {
                'title': _('Next Activity'),
                'next_activity': log.x_partnernext_activity_id.name,
                'x_partner': log.id,  # **dwi nambah ini
                'description': log.x_partnertitle_action and '<p><em>%s</em></p>' % log.x_partnertitle_action or '',
                'note': log.x_partnernote or '',
            }
            log.message_post(x_type_activity='Next Activity', x_PIC=log.x_PIC_action.id,
                                           x_execute_activity=log.x_partnerdate_deadline,
                                           x_next_activity=log.x_partnernext_activity_id.id, x_partner=log.id,
                                           subject=log.x_partnertitle_action)

            calendar_event = self.env['calendar.event']
            calendar_event.create({
                'name': log.x_partnernext_activity_id.name + " for " + log.name,
                'partner_ids': [(4, log.x_PIC_action.partner_id.id)],
                'start_datetime': log.x_partnerdate_deadline,
                'start': log.x_partnerdate_deadline,
                'stop': log.x_partnerdate_deadline,
                'alarm_ids': [(4, 1)],
            #     # 'company_id': self.company_id.id,
            })

            #######KIRIM EMAIL APPOINMENT
            if log.x_partnernext_activity_id.x_type_activity == 'visit':
                template = self.env.ref('lpj_cusrequire.template_mail_test_employee')
                mail = self.env['mail.template'].browse(template.id)
                mail.send_mail(self.id, force_send=True) #langsung kirim email


        # return result

    @api.multi
    def send_notif_apoin(self):
        template = self.env.ref('lpj_cusrequire.template_mail_test_employee')
        mail = self.env['mail.template'].browse(template.id)
        mail.send_mail(self.id, force_send=True)

class estimated_product(models.Model):
    _name = 'x.estimated.product.crm'
    x_qty = fields.Integer(string = 'estimated quantity')
    x_uom = fields.Many2one('product.uom', string = 'Unit of Measure')
    x_crm_lead = fields.Many2one('crm.lead', string='CRM Lead')
    x_product_product_crm = fields.Many2one('x.product.product.crm', string='Estimated Product')
    x_desc = fields.Text (string = 'Description')
    x_flag_harga = fields.Boolean(string = 'flag sudah create SQ', default = False)

    @api.multi
    def crm_sq(self):
        self.x_flag_harga = True
        ac = self.env['ir.model.data'].xmlid_to_res_id('lpj_cusrequire.x_sq_view', raise_if_not_found=True)
        # for o in self:
        result = {
            'name': 'Sales Quotation',
            'view_type': 'form',
            'res_model': 'x.sales.quotation',
            'view_id': ac,
            'context': {
                # 'default_name': sq
            },
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'current',
        }
        return result


class product_product_crm(models.Model):
    _name = 'x.product.product.crm'

    x_name = fields.Char(string = 'Product Name')
    x_length = fields.Float(string = 'Length (mm)')
    x_length_m = fields.Float(readonly=True, store=True)
    x_width = fields.Float(string='Width (mm)')
    x_width_m = fields.Float(readonly=True, store=True)
    # x_description = fields.Text (string = 'Description')
    x_sample_product = fields.Binary(string = 'Sample Product')


    @api.onchange("x_length", "x_width")
    def check_konversi(self):
        if self.x_length > 0:
            self.x_length_m = self.x_length / 1000
        if self.x_width > 0:
            self.x_width_m = self.x_width / 1000

class crm_activities_inherit(models.Model):
    _inherit = 'crm.activity'

    x_type_activity = fields.Selection([('others', 'Others'), ('visit', 'Visit')], default='others', string="Type Activity")


# class temporary_cust_state(models.Model):
#     _name = 'x.cust.state'
#
#     x_name = fields.Many2one('x.cusrequirement', string = 'SQ')
#     x_state = fields.Many2one('crm.stage',string = 'Stage')


class lead_status(models.Model):
    _name = 'x.lead.status'

    name = fields.Char(string = 'Nama')


class lead_source(models.Model):
    _name = 'x.lead.source'

    name = fields.Char(string='Nama')