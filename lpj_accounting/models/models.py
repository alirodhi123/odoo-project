# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
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


class Kuitansi (models.Model):
    _name = 'x.kuitansi'

    # Wizard kuitansi
    def _default_invoice(self):
        return self.env['account.invoice'].browse(self._context.get('active_id'))

    name = fields.Char(string="No", readonly=True)
    invoice_id = fields.Many2one('account.invoice', string="Invoice", required=True, default=_default_invoice)
    customer = fields.Many2one('res.partner', string="Customer", related='invoice_id.partner_id', required = True)
    kuitansi_line_ids = fields.One2many('x.kuitansi.line', 'kuitansi_id', string="Kuitansi Line")
    currency_id = fields.Many2one(related="kuitansi_line_ids.currency_id")
    company_id = fields.Many2one('res.company', string='Company', change_default=True, required=True, readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env['res.company']._company_default_get('kuitansi_line_ids.x_invoice'))
    x_amount_temp = fields.Many2one(related="kuitansi_line_ids.x_invoice")
    tgl_invoice = fields.Date(string="Invoice Date", default=datetime.today())

     
    # Sequences
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('seq.kuitansi') or ('New')

        for o in vals['kuitansi_line_ids']:
            fg = o[2]['x_invoice']

            account = self.env['account.invoice'].search([('id', '=', fg)])
            account.write({'is_responsible': True})

        return super(Kuitansi, self).create(vals)

    # Menjumlahkan untaxed amount, taxes, amount total
    @api.one
    @api.depends('kuitansi_line_ids.x_amount_untaxed', 'kuitansi_line_ids.x_taxes',
                 'kuitansi_line_ids.x_amount_total', 'kuitansi_line_ids.x_total_jasa', 'kuitansi_line_ids.x_total_material',
                 'kuitansi_line_ids.x_diskon', 'kuitansi_line_ids.x_bruto_kwt')
    def _compute_amount(self):
        amount_untaxed = 0
        taxes = 0
        amount_total = 0
        total_jasa = 0
        total_material = 0
        diskon = 0
        bruto = 0

        for m in self.kuitansi_line_ids:
            amount_untaxed += m.x_amount_untaxed
            taxes += m.x_taxes
            amount_total += m.x_amount_total
            total_jasa += m.x_total_jasa
            total_material += m.x_total_material
            diskon += m.x_diskon
            bruto += m.x_bruto_kwt

        self.x_untaxed_amount_foot = amount_untaxed
        self.x_amount_tax_foot = taxes
        self.x_amount_total_foot = amount_total
        self.x_total_jasa_foot = total_jasa
        self.x_total_material_foot = total_material
        self.x_diskon_foot = diskon
        self.x_bruto_kwt_foot = bruto

    x_untaxed_amount_foot = fields.Monetary(string='Untaxed Amount', compute='_compute_amount', readonly=True)
    x_amount_tax_foot = fields.Monetary(string='Tax', readonly=True, compute='_compute_amount')
    x_amount_total_foot = fields.Monetary(string='Total', readonly=True, compute='_compute_amount')
    x_total_jasa_foot = fields.Monetary(string='Total Service', readonly=True, compute='_compute_amount')
    x_total_material_foot = fields.Monetary(string='Total Material', readonly=True, compute='_compute_amount')
    x_diskon_foot = fields.Monetary(string="Discount", readonly=True, compute='_compute_amount')
    x_bruto_kwt_foot = fields.Monetary(string="Bruto", readonly=True, compute='_compute_amount')

    @api.one
    @api.depends('x_amount_total_foot')
    def _amount_in_word(self):
        self.amount_to_text = terbilang(self.x_amount_total_foot, 'idr', 'id')

    amount_to_text = fields.Text(string="Terbilang", store=True, readonly=True,
                                 compute='_amount_in_word')


class kuitansi_line(models.Model):
    _name = 'x.kuitansi.line'

    kuitansi_id = fields.Many2one('x.kuitansi', ondelete='cascade')
    x_invoice_line = fields.Many2one('account.invoice.line')
    x_invoice = fields.Many2one('account.invoice', string="Invoice ID")
    x_amount_untaxed = fields.Monetary(string='Amount Untaxed', related='x_invoice.amount_untaxed')
    x_taxes = fields.Monetary(string="Taxes", related="x_invoice.amount_tax")
    x_amount_total = fields.Monetary(string='Amount Total', related='x_invoice.amount_total')
    currency_id = fields.Many2one('res.currency', related='x_invoice.currency_id', store=True, readonly=True)
    is_responsible = fields.Boolean(string="Kuitansi Status", default=False)
    x_no_sjk = fields.Many2one('stock.picking', string="No SJK", related='x_invoice.x_no_sjk', readonly=True)
    date_sjk = fields.Date(related='x_invoice.x_tanggal_sjk')
    x_no_faktur = fields.Char(related='x_invoice.x_no_faktur')
    date_invoice = fields.Date(related='x_invoice.date_invoice')
    x_total_jasa = fields.Monetary(related='x_invoice.x_total_jasa', string="Harga Service")
    x_total_material = fields.Monetary(related='x_invoice.x_total_material', string="Harga Material")
    x_diskon = fields.Monetary(related='x_invoice.x_discount_foot', string="Discount")
    x_bruto_kwt = fields.Monetary(related='x_invoice.x_bruto')




