from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta


class x_attendance(models.Model):
    _name = 'x.attendance'

    x_employee = fields.Many2one('hr.employee', string="Employee")
    x_checkin = fields.Datetime(string="Check In")
    x_checkout = fields.Datetime(string="Check Out")
    x_date_of_entry = fields.Date(string="Date of Entry")
    x_badge_id_temp = fields.Char(string="Badge Id")
    x_categ_in = fields.Char(string="Category In")
    x_categ_out = fields.Char(string="Category Out")
    x_checkin_view = fields.Datetime(string="Check In View")
    x_checkout_view = fields.Datetime(string="Check Out View")
    x_validate = fields.Boolean(default=False)
    x_selisih_masuk = fields.Char(string="Selisih Masuk")
    x_selisih_pulang = fields.Char(string="Selisih Pulang")


    # Konversi badge_id menjadi id employee
    @api.constrains('x_badge_id_temp')
    def _check_validity_employee_temp(self):
        for attendance in self:
            badge_id = attendance.x_badge_id_temp
            employee = self.env['hr.employee'].search([('pin', '=', badge_id)])
            if employee:
                for row in employee:
                    pin = row.pin
                    employee_id = row.id

                    if pin == badge_id:
                        attendance.update({'x_employee': employee_id})
                    else:
                        pass

    @api.constrains('x_employee')
    def _check_double_data(self):
        for attendance in self:
            employee = attendance.x_employee
            checkin = attendance.x_checkin
            date_format = "%Y-%m-%d"

            self.env.cr.execute("SELECT * FROM x_attendance "
                                "WHERE x_employee = '"+ str(employee.id) +"' "
                                "AND to_char(x_checkin, 'YYYY-MM-DD') = to_char('"+ str(checkin) +"', 'YYYY-MM-DD')")

            data = self.env.cr.fetchone()
            if data:
                var = "SUKSES"









