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
    x_mesin_shift = fields.Many2one('x.shift.mesin', string="Mesin")

    # Klik button insert shift
    @api.multi
    def insert_shift(self):
        self.delete_shift()
        date_start = self.x_start_date
        date_end = self.x_end_date
        mesin = self.x_mesin_shift
        hours = 24
        terms = []

        if date_start:
            format_date = datetime.strptime(str(date_start), '%Y-%m-%d')
            for row in range(13):
                values = {}

                values['x_mesin_id'] = mesin.id
                values['x_date'] = format_date
                format_date = format_date + relativedelta(hours=float(hours))

                terms.append((0, 0, values))

            return self.update({'x_shift_employee_ids': terms})

    @api.multi
    def delete_shift(self):
        shift_line_ids = []
        id = self.id

        shift = self.env['x.shift.employee'].search([('id', '=', id)])
        if shift:
            for row in shift:
                shift_line_ids.append(([5]))

                return self.update({'x_shift_employee_ids': shift_line_ids})


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