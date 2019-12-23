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
            'url': 'http://192.168.1.15:8038/',
        }
        return result

