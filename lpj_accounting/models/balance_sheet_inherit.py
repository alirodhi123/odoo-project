from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import amount_to_text_en, datetime, timedelta
from odoo.tools import amount_to_text
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class BalanceSheet(models.TransientModel):
    _inherit = 'accounting.report'

    @api.multi
    def check_report_xls(self):
        return self.env['report'].get_action(self, 'lpj_accounting.balance_sheet_report.xlsx')