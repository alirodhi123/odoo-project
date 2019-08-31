from odoo import models, fields, api
from datetime import datetime


class WizardAbsensi(models.Model):
    _name = 'x.popup.absensi'

    @api.model
    def _get_default_name(self):
        name = "192.168.1.7"
        return name

    @api.model
    def _get_default_db_name(self):
        name = "Att2000"
        return name

    @api.model
    def _get_default_db_server(self):
        name = "MSSql"
        return name

    name = fields.Char(string="IP", default=_get_default_name)
    x_db_name = fields.Char(string="Database Name", default=_get_default_db_name)
    x_db_server = fields.Char(string="DBMS", default=_get_default_db_server)


    @api.multi
    def open_url(self):
        result = {
            'name': '2nd class',
            'res_model': 'ir.actions.act_url',
            'type': 'ir.actions.act_url',
            'view_mode': 'form',
            'url': 'http://127.0.0.1:8000/',
        }
        return result

    @api.multi
    def get_employee_not_here(self):
        for attendance in self:
            attendance.env.cr.execute("SELECT he.name_related, attend.x_checkin "
                                      "FROM hr_employee he "
                                      "LEFT JOIN x_attendance attend on attend.x_employee = he.id "
                                      "WHERE he.id = '" + str(employee.id) + "'")
            var = attendance.env.cr.fetchall()
            if var:
                for row in var:
                    employee_name = row[0]
                    checkin_checkin = row[1]