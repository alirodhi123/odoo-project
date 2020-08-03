
from odoo import models, fields, api, _
from odoo.tools import amount_to_text_en, datetime, timedelta
from odoo.tools import amount_to_text
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from datetime import datetime


class stockPicking(models.Model):
    _inherit = 'stock.picking'

    is_responsible = fields.Boolean(string="SJK Status", default=False)
    x_confirmation_sjk = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                          default='no', readonly=True, string="Confirmation SJK")
    x_confirmation_date = fields.Datetime(string="Confirmation Date")



    # Fungsi agar x_confirmation_sjk No ketika create backorder
    def copy(self, default=None):
        default = dict(default or {})
        default.update({
            'x_confirmation_sjk': 'no',
        })
        return super(stockPicking, self).copy(default)

    @api.multi
    def sjk_confirmatipn(self):
        for picking in self:
            picking.update({
                'x_confirmation_sjk': 'yes',
                'x_confirmation_date': datetime.now()
            })