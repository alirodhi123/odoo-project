from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar


class ShiftEmployee(models.Model):
    _name = 'x.shift.employee'

    x_shift_employee_ids = fields.One2many('x.shift.employee.line', 'x_shift_employee_id', string="Shift Line")
    x_employee = fields.Many2one('hr.employee', string="Employee Name")
    x_start_date = fields.Date(string="Date Start")
    x_end_date = fields.Date(string="Date End")

    # Klik button insert shift
    def insert_shift(self):
        date_start = self.x_start_date
        date_end = self.x_end_date
        hours = 24

        if date_start:
            for row in range(2):
                coba_date = date_start

                format_date = datetime.strptime(str(coba_date), '%Y-%m-%d') + relativedelta(hours=float(hours))

                var = format_date


class ShiftEmployeeLine(models.Model):
    _name = 'x.shift.employee.line'

    x_shift_employee_id = fields.Many2one('x.shift.employee', ondelete='cascade')
    x_date = fields.Date(string="Date")
    x_shift_id = fields.Many2one('x.master.shift', string="Shift")
    x_mesin_id = fields.Many2one('x.shift.mesin', string="Mesin")



class MasterShiftEmployee(models.Model):
    _name = 'x.master.shift'

    x_name = fields.Char(string="Shift")
    x_jam_masuk = fields.Float(string="Jam Masuk")
    x_jam_pulang = fields.Float(string="Jam Pulang")