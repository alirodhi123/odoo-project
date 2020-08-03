# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, SUPERUSER_ID, _
import re
from datetime import date
from datetime import datetime
from odoo import netsvc
from dateutil.relativedelta import relativedelta

from odoo.exceptions import AccessError


class HelpdeskTicket(models.Model):
    _name = "helpdesk_lite.ticket"
    _description = "Helpdesk Tickets"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _order = "priority desc, create_date desc"
    _mail_post_access = 'read'

    @api.model
    def _get_default_stage_id(self):
        return self.env['helpdesk_lite.stage'].search("", order='sequence', limit=1)

    @api.model
    def _get_default_requested_by(self):
        return self.env['res.users'].browse(self.env.uid)

    category_masalah_ids = fields.One2many('helpdesk.lite.line', 'helpdesk_id', string="Detail Problem")

    # uswa-tambah 'parts_list_ids'
    parts_list_ids = fields.One2many('parts.helpdesk.line', 'helpdesk_parts_id', string="Parts")


    name = fields.Char(string='Ticket', track_visibility='always', required=True)
    description = fields.Text('Private Note')
    partner_id = fields.Many2one('res.partner', string='Customer', track_visibility='onchange', index=True)
    contact_name = fields.Char('Contact Name')
    email_from = fields.Char('Email', help="Email address of the contact", index=True)
    user_id = fields.Many2one('res.users', string='Assigned to', track_visibility='onchange',
                              index=True, default=24, required=True)
    team_id = fields.Many2one('helpdesk_lite.team', string='Support Team', track_visibility='onchange',
        default=lambda self: self.env['helpdesk_lite.team'].sudo()._get_default_team_id(user_id=self.env.uid),
        index=True, help='When sending mails, the default email address is taken from the support team.')
    date_deadline = fields.Datetime(string='Deadline', track_visibility='onchange')

    stage_id = fields.Many2one('helpdesk_lite.stage', string='Stage', index=True, track_visibility='onchange',
                               domain="[]",
                               copy=False,
                               group_expand='_read_group_stage_ids',
                               default=_get_default_stage_id)
    priority = fields.Selection([('0', 'Low'), ('1', 'Normal'), ('2', 'High'), ('3', 'Urgent')], 'Priority', index=True, default='1', track_visibility='onchange')
    kanban_state = fields.Selection([('normal', 'Normal'), ('blocked', 'Blocked'), ('done', 'Ready for next stage')], string='Kanban State', track_visibility='onchange',
                                    required=True, default='normal',
                                    help="""A Ticket's kanban state indicates special situations affecting it:\n
                                           * Normal is the default situation\n
                                           * Blocked indicates something is preventing the progress of this ticket\n
                                           * Ready for next stage indicates the ticket is ready to go to next stage""")

    color = fields.Integer('Color Index')
    legend_blocked = fields.Char(related="stage_id.legend_blocked", string='Kanban Blocked Explanation', readonly=True)
    legend_done = fields.Char(related="stage_id.legend_done", string='Kanban Valid Explanation', readonly=True)
    legend_normal = fields.Char(related="stage_id.legend_normal", string='Kanban Ongoing Explanation', readonly=True)

    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    request_by = fields.Many2one('res.users', 'Requested by', required=True, track_visibility='onchange',
                                   default=_get_default_requested_by)
    no_ticket = fields.Char(string="No Ticket", readonly=True)
    category_ticket = fields.Many2one('categ.ticket', string="Category Ticket")
    type_ticket = fields.Selection([('permintaan_perbaikan', 'Permintaan Perbaikan'),
                                    ('laporan_problem', 'Laporan Problem'),
                                    ('ajukan_pertanyaan', 'Ajukan Pertanyaan'),
                                    ('permintaan_pengembangan', 'Permintaan Pengembangan')], string="Type Ticket")
    state = fields.Selection([('1', 'Draft'),
                              ('2', 'New Ticket'),
                              ('3', 'In Progress'),
                              ('4', 'Solved'),
                              ('5', 'Done'),
                              ('6', 'Pending'),
                              ('7', 'Canceled')], string="State", default='1', track_visibility='onchange')
    start_date = fields.Date(string="Start Date", readonly=True)
    finish_date = fields.Date(string="Finish Date", readonly=True)
    verification_date = fields.Date(string="Validation Date", readonly=True)
    selisih_date = fields.Integer(string="Duration Finish", compute='selisih_tanggal')
    duration_verification_date = fields.Integer(string="Duration Verification", compute='selisih_tanggal')
    total_pengerjaan = fields.Integer(string="Total Duration", compute='total_duration')
    x_request_id = fields.Many2one('res.users', string='Request By', readonly=True, index=True, track_visibility='onchange',
                                default=lambda self: self.env.user)
    procurement_group_id = fields.Many2one('procurement.group', 'Procurement group', copy=False)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """ This function sets partner email address based on partner
        """
        self.email_from = self.partner_id.email

    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        default.update(name=_('%s (copy)') % (self.name))
        return super(HelpdeskTicket, self).copy(default=default)

    @api.multi
    def message_get_suggested_recipients(self):
        recipients = super(HelpdeskTicket, self).message_get_suggested_recipients()
        try:
            for tic in self:
                if tic.partner_id:
                    tic._message_add_suggested_recipient(recipients, partner=tic.partner_id, reason=_('Customer'))
                elif tic.email_from:
                    tic._message_add_suggested_recipient(recipients, email=tic.email_from, reason=_('Customer Email'))
        except AccessError:  # no read access rights -> just ignore suggested recipients because this imply modifying followers
            pass
        return recipients

    @api.model
    def message_new(self, msg, custom_values=None):
        """ Overrides mail_thread message_new that is called by the mailgateway
            through message_process.
            This override updates the document according to the email.
        """
        # remove default author when going through the mail gateway. Indeed we
        # do not want to explicitly set user_id to False; however we do not
        # want the gateway user to be responsible if no other responsible is
        # found.
        contact_name, email_from =  re.match(r"(.*) *<(.*)>", msg.get('from')).group(1,2)
        body = tools.html2plaintext(msg.get('body'))
        bre = re.match(r"(.*)^-- *$", body, re.MULTILINE|re.DOTALL|re.UNICODE)
        if bre:
            desc = bre.group(1)
        defaults = {
            'name':  msg.get('subject') or _("No Subject"),
            'email_from': email_from,
            'contact_name': contact_name,
            'description':  desc or body,
        }

        create_context = dict(self.env.context or {})
        # create_context['default_user_id'] = False
        # create_context.update({
        #     'mail_create_nolog': True,
        # })

        if custom_values:
            defaults.update(custom_values)

        return super(HelpdeskTicket, self.with_context(create_context)).message_new(msg, custom_values=defaults)
        # res_id = super(HelpdeskTicket, self.with_context(create_context)).message_new(msg, custom_values=defaults)
        # tic = self.browse(res_id)
        # email_list = tools.email_split(email_from)
        # partner_ids = filter(None, tic._find_partner_from_emails(email_list))
        # tic.message_subscribe(partner_ids)
        # return res_id

    @api.model
    def create(self, vals):

        vals['no_ticket'] = self.env['ir.sequence'].next_by_code('seq.ticket') or ('New')

        partner_id = vals.get('partner_id')
        email_from = vals.get('email_from')
        if not partner_id:
            partner = self.env['res.partner'].sudo().search([('email', '=ilike', email_from)], limit=1)
            partner_id = partner.id
            if partner_id:
                vals.update({
                    'partner_id': partner_id,
                })
                del vals['contact_name']
        # if partner_id:
        #     vals.update({
        #         'message_follower_ids': [(4, partner_id)]
        #         })

        context = dict(self.env.context)
        context.update({
            'mail_create_nosubscribe': True,
        })
        # self.message_subscribe([partner_id])
        return super(HelpdeskTicket, self.with_context(context)).create(vals)


    @api.multi
    def write(self, vals):
        # stage change: update date_last_stage_update
        if 'stage_id' in vals:
            # vals.update(vals['stage_id'])
            if 'kanban_state' not in vals:
                vals['kanban_state'] = 'normal'
        # user_id change: update date_open
        # if vals.get('user_id') and 'date_open' not in vals:
        #     vals['date_open'] = fields.Datetime.now()
        return super(HelpdeskTicket, self).write(vals)

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):

        search_domain = []

        # perform search
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    # Tidak dipakai
    @api.multi
    def takeit(self):
        self.ensure_one()
        vals = {'user_id' : self.env.uid,
                'team_id': self.env['helpdesk_lite.team'].sudo()._get_default_team_id(user_id=self.env.uid).id}
        return super(HelpdeskTicket, self).write(vals)


    # Action button request
    @api.multi
    def request(self):
        return self.update({'state': '2'})

    # Action button take it ticket
    @api.multi
    def takeit_new(self):

        # kode ali ori
        # return \
        # self.update({
        #     'state': '3',
        #     'start_date': date.today()
        # })

        # uswa-tambah koding ini
        stock_move_obj = self.env['stock.move']
        ac = self.env['ir.model.data'].xmlid_to_res_id('stock.view_picking_form', raise_if_not_found=True)
        new_parts_lines = []

        for row in self:
            no_ticket = row.no_ticket
            list_ids = row.parts_list_ids

            if list_ids:
                for line in list_ids:
                    uom = line.parts_uom
                    product = line.parts2_id

                    values = {}
                    values['product_id'] = line.parts2_id.id
                    values['product_uom_qty'] = line.parts_qty
                    values['product_uom'] = uom.id
                    new_parts_lines.append((0, 0, values))

                return stock_move_obj.create({
                    'name': no_ticket,
                    'origin': no_ticket,
                    'location_id': 15,
                    'location_dest_id': 19,
                    'picking_type_id': 5,
                    'product_id': product.id,
                    'product_uom': uom.id,
                    'move_lines': new_parts_lines
                })

            # result = {
            #     'name': 'Drafts Tickets to Solved',
            #     'view_type': 'form',
            #     'res_model': 'stock.picking',
            #     'view_id': ac,
            #     'context': {
            #         'default_origin': no_ticket,
            #         'default_location_id': 15,
            #         'default_location_dest_id': 22,
            #         'default_picking_type_id': 5,
            #         'default_scrapped': True,
            #         'default_move_lines': new_parts_lines,
            #     },
            #     'type': 'ir.actions.act_window',
            #     'view_mode': 'form',
            #     'target': 'current',
            #
            # }




    # Action button solved
    @api.multi
    def solved(self):
        # uswa- tambah ini
        # get parts_id and parts_qty
        # for order in self:
        #     line_parts_ids = []
        #     line_parts_qty = []
        #     if order.parts_list_ids:
        #         for a_parts in order.parts_list_ids:
        #             line_parts_ids += [a_parts.parts2_id]
        #             line_parts_qty += [a_parts.parts_qty]
        #
        #
        # self.force_parts_reservation()
        # # odoo 7
        # wf_service = netsvc.LocalService("workflow")
        # for order in self:
        #     wf_service.trg_validate(self.env.user.id, 'mro.order', order.id, 'solved', self.env.cr)
        # # return True
        #
        #
        # # odoo 10
        # records = self.env['mro.order'].browse(ids)
        # for order in self:
        #     records.signal_workflow('solved')

        # wf_service = netsvc.LocalService('workflow')
        # wf_service.trg_validate(uid, 'account.invoice', id, 'invoice_cancel', cr)
        #
        # records = self.env['account.invoice'].browse(ids)
        # records.signal_workflow('invoice_cancel')

    # kode ali ori
        return self.update({
            'state': '4',
            'finish_date': date.today()
        })

        # Action button solved

    # uswa-tambah ini
    # def _get_available_parts(self):
    #     for order in self:
    #         line_ids = []
    #         available_line_ids = []
    #         done_line_ids = []
    #         if order.procurement_group_id:
    #             for procurement in order.procurement_group_id.procurement_ids:
    #                 line_ids += [move.id for move in procurement.move_ids if
    #                              move.location_dest_id.id == order.asset_id.property_stock_asset.id]
    #                 available_line_ids += [move.id for move in procurement.move_ids if
    #                                        move.location_dest_id.id == order.asset_id.property_stock_asset.id and move.state == 'assigned']
    #                 done_line_ids += [move.id for move in procurement.move_ids if
    #                                   move.location_dest_id.id == order.asset_id.property_stock_asset.id and move.state == 'done']
    #         order.parts_ready_lines = line_ids
    #         order.parts_move_lines = available_line_ids
    #         order.parts_moved_lines = done_line_ids
    #
    # parts_list_ids = fields.One2many('parts.helpdesk.line', 'helpdesk_parts_id', string="Parts")
    #
    # parts_ready_lines = fields.One2many('stock.move', compute='_get_available_parts')
    # parts_move_lines = fields.One2many('stock.move', compute='_get_available_parts')
    # parts_moved_lines = fields.One2many('stock.move', compute='_get_available_parts')

    # uswa-tambah ini
    def force_parts_reservation(self):
        for order in self:
            order.parts_ready_lines.force_assign()
        return True

    # Action button done
    @api.multi
    def done(self):
        return self.update({
            'state': '5',
            'verification_date': date.today()
        })

    # Action button reset to in progress
    @api.multi
    def reset_to_inprogress(self):
        return self.update({
            'state': '5',
        })

    # Action pending
    @api.multi
    def pending(self):
        return self.update({'state': '6'})

    #Action reset to draft
    @api.multi
    def reset_to_draft(self):
        return self.update({'state': '2'})

    # Action button cancel
    @api.multi
    def cancel(self):
        return self.update({'state': '7'})

    # Menghitung selisih tanggal
    @api.one
    def selisih_tanggal(self):
        for row in self:
            if row.start_date and row.finish_date:
                date_format = "%Y-%m-%d"
                date_start = row.start_date
                date_finish = row.finish_date
                date_verification = row.verification_date

                start_date = datetime.strptime(str(date_start), date_format)
                finish_date = datetime.strptime(str(date_finish), date_format)
                if date_verification != False:
                    verification_date = datetime.strptime(str(date_verification), date_format)
                    # Finish date to verification date
                    selisih_verification = (verification_date - finish_date).days
                    row.duration_verification_date = selisih_verification

                # Start date to finish date
                selisih = (finish_date - start_date).days
                row.selisih_date = selisih


    @api.one
    def total_duration(self):
        for row in self:
            selisih_date = row.selisih_date
            verification_date = row.duration_verification_date

            hasil = selisih_date + verification_date
            row.total_pengerjaan = hasil



class helpdesk_lite_line(models.Model):
    _name = 'helpdesk.lite.line'

    helpdesk_id = fields.Many2one('helpdesk_lite.ticket')
    categ_id = fields.Many2one('categ.problem', string="Detail Problem")
    problem_description = fields.Text(string="Problem Description")








