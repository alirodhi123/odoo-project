from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta


class x_attendance_attendance(models.Model):
    _name = 'x.attendance.attendance'

    x_employee_attend = fields.Many2one('hr.employee', string="Emloyee")
    x_check_in_attend = fields.Datetime(string="Check In")
    x_check_out_attend = fields.Datetime(string="Check Out")
    x_categ_in_attend = fields.Char(string="Category In")
    x_categ_out_attend = fields.Char(string="Category Out")
    state_attend = fields.Selection([('draft', 'Draft'), ('validate', 'Validated')], default='draft')
    x_check_in_view_attend = fields.Datetime(string="Check In View")
    x_check_out_view_attend = fields.Datetime(string="Check Out View")
    x_date_attend = fields.Date(string="Date")
    x_id_attend = fields.Integer()
    x_to_varchar_attend = fields.Char(string="Format Tanggal")
    x_contract_type_attend = fields.Char(string="Contract Type")
    x_selisih_pulang_attend = fields.Char(string="Selisih Keluar")
    x_selisih_masuk_attend = fields.Char(string="Selisih Masuk")
    x_department_attend = fields.Char(string="Department")






