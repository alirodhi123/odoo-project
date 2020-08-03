
from odoo import models, fields, api
# import odoo.addons.decimal_precision as dp


class inherit_contact_partner(models.Model):

     _inherit = 'res.partner'

     x_rt = fields.Char(string = 'RT')
     x_rw = fields.Char(string='RW')
     x_npwp = fields.Char(string = 'NPWP', readonly=True)
     x_pkp = fields.Boolean(string = 'PKP')
     x_kode_customer = fields.Char(string ='kode customer')
     x_pipeline_customer = fields.Char(string='Pipeline Customer', compute = 'x_state_cust')
     x_state_customer = fields.Char(string = 'jangan dihapus')
     x_status_cust = fields.Char(string='Customer Potential', readonly=True)
     x_tamp_pipeline = fields.Char(string = 'Tampungan pipeline',related = 'x_pipeline_customer', store = True)

     # fields untuk ambil data history

     x_customer_service = fields.Many2one('res.users',string = 'Customer Services')
     x_next_activity_id = fields.Many2one('crm.activity', 'Next Activity', track_visibility='always')
     x_activity = fields.Many2one('crm.activity', 'Activity', track_visibility='always')
     x_date_action = fields.Datetime('Next Activity Date', track_visibility='always')
     x_propose = fields.Char(track_visibility='always', string = 'Next Activity Purpose')
     x_activity = fields.Many2one('crm.activity', 'Activity', track_visibility='always')
     x_summary = fields.Char(string='Summary', track_visibility='always')
     x_expected_revenue = fields.Float(string='Expected Revenue', track_visibility='always')
     x_expected_closing = fields.Datetime(string='Expected Closing', track_visibility='always')
     x_description = fields.Html('Note(s)', track_visibility='always')
     x_history_act = fields.One2many('x.history.activity', 'name',string = 'History Activity')

     @api.one
     def x_state_cust(self):
         self.env.cr.execute("select pipeline_customer ('" + str(self.id) + "')")

     # @api.one
     # def status_customer(self):
     #      # self.x_pipeline_customer = 'AAAAA'
     #      self.env.cr.execute("select distinct (cs.name) from crm_lead cl "
     #                          "left join res_partner rp on cl.partner_id = rp.id "
     #                          "left join crm_stage cs on cl.stage_id = cs.id "
     #                          "where cl.stage_id = (select max(stage_id) from crm_lead where partner_id =" + str(self.id) + ")")
     #      cus = self.env.cr.fetchone()
     #      if cus:
     #           self.x_pipeline_customer = cus[0]


     # @api.onchange('x_pipeline_customer')
     # def _tamp_pipeline(self):
     #      self.x_tamp_pipeline = self.x_pipeline_customer

class termin_line(models.Model):
     _name = 'x.termin'

     name = fields.Char(string = 'Nama Termin')
     Description = fields.Text(string = 'Description')

class x_history_act(models.Model):
     _name = 'x.history.activity'

     name = fields.Many2one('res.partner', string = 'Partner')
     x_history_activity = fields.Char(string='History Activity', compute='get_history_activity')
     x_history_summary = fields.Char(string='History Summary')
     x_history_description = fields.Char(string='History Description')
     x_exec_date = fields.Char(string='History Execution Date')
     x_deadline = fields.Char(string='History Deadline')
     x_next_actv = fields.Char(string='History Next Activity')
     x_date_action = fields.Char(string='History Date Action')

     @api.one
     def get_history_activity(self):
          self._cr.execute("select mm.subject from mail_message mm"
                              " left join res_partner rp on cast(mm.x_partner as integer) = rp.id"
                              " where rp.id = 2220")
          history = self._cr.fetchall()

          for a in history:
               self.x_history_summary = self.x_history_summary  + '  ' + a
               # self.x_history_activity = a[0]

               # self.x_history_description = a.history[2]
               # self.x_exec_date = a.history[3]
               # self.x_deadline = a.history[4]
               # self.x_next_actv = a.history[5]
               # self.x_date_action = a.history[6]

