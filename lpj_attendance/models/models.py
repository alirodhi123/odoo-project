# -*- coding: utf-8 -*-

from odoo import models, fields, api
#
class Attendance(models.Model):
    _inherit = 'hr.attendance'

    x_checkin_view_hr = fields.Datetime(string="Check In View")
    x_checkout_view_hr = fields.Datetime(string="Check Out View")
    x_categ_in_hr = fields.Char(string="Category In")
    x_categ_out_hr = fields.Char(string="Category Out")
    x_department_hr = fields.Char(string="Department")
    x_contract_type_hr = fields.Char(string="Contract Type")
    x_format_tanggal_hr = fields.Char(string="Format Tanggal")
    x_selisih_masuk_hr = fields.Char(string="Selisih Masuk")
    x_selisih_pulang_hr = fields.Char(string="Selisih Pulang")










