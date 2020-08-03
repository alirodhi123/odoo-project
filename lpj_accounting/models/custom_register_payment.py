from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import amount_to_text_en, datetime, timedelta
from odoo.tools import amount_to_text
from datetime import timedelta
from dateutil.relativedelta import relativedelta


dic = {
    'to_19': ('Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve',
              'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen'),
    'tens': ('Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety'),
    'denom': ('', 'Thousand', 'Million', 'Billion', 'Trillion', 'Quadrillion', 'Quintillion'),
    'to_19_id': (
    'Nol', 'Satu', 'Dua', 'Tiga', 'Empat', 'Lima', 'Enam', 'Tujuh', 'Delapan', 'Sembilan', 'Sepuluh', 'Sebelas',
    'Dua Belas', 'Tiga Belas', 'Empat Belas', 'Lima Belas', 'Enam Belas', 'Tujuh Belas', 'Delapan Belas',
    'Sembilan Belas'),
    'tens_id': ('Dua Puluh', 'Tiga Puluh', 'Empat Puluh', 'Lima Puluh', 'Enam Puluh', 'Tujuh Puluh', 'Delapan Puluh',
                'Sembilan Puluh'),
    'denom_id': ('', 'Ribu', 'Juta', 'Miliar', 'Triliun', 'Biliun')
}


def terbilang(number, currency, bhs):
    number = '%.2f' % number
    units_name = ' ' + cur_name(currency) + ' '
    lis = str(number).split('.')
    start_word = english_number(int(lis[0]), bhs)
    end_word = english_number(int(lis[1]), bhs)
    cents_number = int(lis[1])
    cents_name = (cents_number > 1) and 'Sen' or 'sen'
    final_result_sen = start_word + units_name + end_word + ' ' + cents_name
    final_result = start_word + units_name
    if end_word == 'Nol' or end_word == 'Zero':
        final_result = final_result
    else:
        final_result = final_result_sen

    return final_result[:1].upper() + final_result[1:]


def _convert_nn(val, bhs):
    tens = dic['tens_id']
    to_19 = dic['to_19_id']
    if bhs == 'en':
        tens = dic['tens']
        to_19 = dic['to_19']
    if val < 20:
        return to_19[val]
    for (dcap, dval) in ((k, 20 + (10 * v)) for (v, k) in enumerate(tens)):
        if dval + 10 > val:
            if val % 10:
                return dcap + ' ' + to_19[val % 10]
            return dcap


def _convert_nnn(val, bhs):
    word = '';
    rat = ' Ratus';
    to_19 = dic['to_19_id']
    if bhs == 'en':
        rat = ' Hundred'
        to_19 = dic['to_19']
    (mod, rem) = (val % 100, val // 100)
    if rem == 1:
        word = 'Seratus'
        if mod > 0:
            word = word + ' '
    elif rem > 1:
        word = to_19[rem] + rat
        if mod > 0:
            word = word + ' '
    if mod > 0:
        word = word + _convert_nn(mod, bhs)
    return word


def english_number(val, bhs):
    denom = dic['denom_id']
    if bhs == 'en':
        denom = dic['denom']
    if val < 100:
        return _convert_nn(val, bhs)
    if val < 1000:
        return _convert_nnn(val, bhs)
    for (didx, dval) in ((v - 1, 1000 ** v) for v in range(len(denom))):
        if dval > val:
            mod = 1000 ** didx
            l = val // mod
            r = val - (l * mod)
            ret = _convert_nnn(l, bhs) + ' ' + denom[didx]
            if r > 0:
                ret = ret + ' ' + english_number(r, bhs)
            if bhs == 'id':
                if val < 2000:
                    ret = ret.replace("Satu Ribu", "Seribu")
            return ret


def cur_name(cur="idr"):
    cur = cur.lower()
    if cur == "usd":
        return "Dollars"
    elif cur == "aud":
        return "Dollars"
    elif cur == "idr":
        return "Rupiah"
    elif cur == "jpy":
        return "Yen"
    elif cur == "sgd":
        return "Dollars"
    elif cur == "usd":
        return "Dollars"
    elif cur == "eur":
        return "Euro"
    else:
        return cur

class register_payment(models.Model):
    _name = 'x.register.payment'

    name = fields.Char()
    currency_id = fields.Many2one('res.currency', store=True, readonly=True)
    x_vendor = fields.Many2one('res.partner', string='Vendor', readonly=True)
    x_payment_date = fields.Date(string="Payment Date")
    x_memo = fields.Char(string="Memo")
    x_register_payment_line = fields.One2many('x.register.payment.line', 'x_register_payment_id')
    x_account_bank = fields.Many2one('account.account', string="Account Bank")
    x_untaxed_amount_foot = fields.Monetary(string="Untaxed Amount", compute='_compute_amount', store=True)
    x_tax_foot = fields.Monetary(string="Tax", compute='_compute_amount', store=True)
    x_total_amount_foot = fields.Monetary(string="Total", compute='_compute_amount')
    x_tampilan_amount = fields.Float(compute='tampilan_amount')
    x_flag_paid = fields.Boolean(default=False)


    @api.model
    def create(self, vals):
        res = super(register_payment, self).create(vals)

        # Sequence
        sequence = self.env['ir.sequence'].next_by_code('sequence.x.regis.payment.draft') or ('New')
        res.update({'name': sequence})

        return res

    # Button payment action
    @api.multi
    def payment_action(self):
        obj_bill = self.env['account.invoice']

        custom_payment_line = self.x_register_payment_line
        for row in custom_payment_line:
            bill_id = row.x_no_bill

            search_bill_id = obj_bill.search([('id', '=', bill_id.id)])
            if search_bill_id:
                search_bill_id.write({'x_custom_payment_id': self.id})

        return self.env['report'].get_action(self, 'lpj_accounting.custom_report_payment')

    @api.one
    @api.depends('x_register_payment_line.x_untaxed_amount_payment', 'x_register_payment_line.x_tax_payment',
                 'x_register_payment_line.x_total_payment')
    def _compute_amount(self):
        amount_untaxed = 0
        taxes = 0
        amount_total = 0

        for m in self.x_register_payment_line:
            amount_untaxed += m.x_untaxed_amount_payment
            taxes += m.x_tax_payment
            amount_total += m.x_total_payment

        self.x_untaxed_amount_foot = amount_untaxed
        self.x_tax_foot = taxes
        self.x_total_amount_foot = amount_total

    # Untuk fungsi terbilang
    @api.one
    @api.depends('x_total_amount_foot')
    def _amount_in_word(self):
        if self.x_total_amount_foot:
            self.amount_to_text = terbilang(self.x_total_amount_foot, 'idr', 'id')

    amount_to_text = fields.Text(string="Terbilang", store=True,
                                 compute='_amount_in_word')

    # Mengambil amount total yang ada di foot
    @api.one
    def tampilan_amount(self):
        var_amount = self.x_total_amount_foot
        self.x_tampilan_amount = var_amount


class register_payment_line(models.Model):
    _name = 'x.register.payment.line'

    x_register_payment_id = fields.Many2one('x.register.payment', ondelete='cascade')
    x_no_bill = fields.Many2one('account.invoice', string="Vendor Bill")
    x_origin = fields.Char(string="Source Document")
    x_account = fields.Many2one('account.account', string="Account")
    x_bill_date = fields.Date(string="Bill Date")
    x_due_date = fields.Date(string="Due Date")
    currency_id = fields.Many2one('res.currency', readonly=True)
    x_untaxed_amount_payment = fields.Monetary(string="Untaxed Amount")
    x_tax_payment = fields.Monetary(string="Tax")
    x_total_payment = fields.Monetary(string="Total")
    x_tampungan_payment = fields.Float(compute='get_total_amount')

    # Mengambil nilai amount total yang ada di line
    @api.one
    def get_total_amount(self):
        self.x_tampungan_payment = self.x_total_payment
