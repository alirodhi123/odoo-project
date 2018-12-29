# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class qa_alert_tinta(models.Model):
     _inherit = 'quality.alert'

     qa_id_tinta = fields.One2many('x.qa.tinta', 'x_qa_tinta', copy=True)
     x_warna = fields.Char(string = 'Warna')
     x_exp_date = fields.Date(string = 'Expired Date')



class qa_tinta(models.Model):
     _name = 'x.qa.tinta'
     x_qa_tinta = fields.Many2one('quality.alert', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)

     x_waktu_qa_tinta = fields.Datetime(string='Waktu QA Tinta', readonly=True, default=lambda self: fields.datetime.now())
     x_user_qa_tinta = fields.Many2one('res.users', 'User QA Tinta', readonly=True, default=lambda self: self.env.user)
     x_warna = fields.Selection([('1', 'Approve'), ('0', 'Reject')], string='Kesesuaian Warna')
     x_exp_date = fields.Selection([('1', 'Approve'), ('0', 'Reject')], string='Expired date kurang dari 1 tahun')
     x_fisik = fields.Selection([('cair', 'Cair'), ('pasta', 'Pasta')], string='Bentuk Fisik Tinta')
     x_mengendap = fields.Selection([('1', 'Approve'), ('0', 'Reject')], string='Tinta Tidak Mengendap')
     x_mengeras = fields.Selection([('1', 'Approve'), ('0', 'Reject')], string='Tinta Tidak Mengeras')








