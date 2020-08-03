from odoo import models, fields, api, _
from datetime import date


class journal_entri(models.Model):
    _inherit = 'account.move'

    x_total_debit = fields.Monetary(compute='sum_debit_credit')
    x_total_credit = fields.Monetary(compute='sum_debit_credit')
    x_count_debit = fields.Integer(compute='_compute_debitcredit_count')
    x_count_credit = fields.Integer(compute='_compute_debitcredit_count')

    @api.one
    def sum_debit_credit(self):
        var_debit = 0
        var_kredit = 0

        for row in self.line_ids:
            var_debit += row.debit
            var_kredit += row.credit

        self.x_total_debit = var_debit
        self.x_total_credit = var_kredit

    @api.multi
    def _compute_debitcredit_count(self):
        debit_i = 0
        credit_i = 0
        for row in self.line_ids:
            if row.debit != 0:
                debit_i += 1
                self.x_count_debit = debit_i
            else:
                credit_i += 1
                self.x_count_credit = credit_i
