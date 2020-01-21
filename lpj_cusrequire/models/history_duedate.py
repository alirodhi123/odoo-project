from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp
from datetime import datetime
from dateutil.relativedelta import relativedelta


class HistoryDueDate(models.Model):
    _name = 'x.history.duedate2'

    x_id_sq = fields.Char()
    x_kode_sq = fields.Char()
    x_app_id = fields.Integer()
    x_tgl_request = fields.Char()
    x_requester = fields.Char()
    x_id_so = fields.Char()
    x_so = fields.Char()
    x_tgl_keputusan = fields.Char()
    x_admin_sq = fields.Char()
    x_status_so = fields.Char()
    x_tgl_reset = fields.Char()
    x_req_tgl_kirim = fields.Char()
    # x_nama_requester = fields.Char(compute = 'nama_req')
    #
    # @api.one
    # def nama_req(self):
    #     id = self.x_requester
    #     self.env.cr.execute("select rp.name from res_users ru "
    #                         "join res_partner rp on rp.id = ru.partner_id "
    #                         "where ru.id = '"+ (id) +"' ")
    #
    #     sql = self.env.cr.fetchone()
    #     if sql:
    #         self.x_nama_requester = sql[0]