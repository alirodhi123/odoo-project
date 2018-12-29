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
    customer = fields.Char(string="Customer", required = True)
    kuitansi_line_ids = fields.One2many('x.kuitansi.line', 'kuitansi_id', string="Kuitansi Line")
    currency_id = fields.Many2one(related="kuitansi_line_ids.currency_id")
    company_id = fields.Many2one('res.company', string='Company', change_default=True, required=True, readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env['res.company']._company_default_get('kuitansi_line_ids.x_invoice'))
    x_amount_temp = fields.Many2one(related="kuitansi_line_ids.x_invoice")

     
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
                 'kuitansi_line_ids.x_amount_total')
    def _compute_amount(self):
        amount_untaxed = 0
        taxes = 0
        amount_total = 0
        for m in self.kuitansi_line_ids:
            amount_untaxed += m.x_amount_untaxed
            taxes += m.x_taxes
            amount_total += m.x_amount_total
        self.x_untaxed_amount_foot = amount_untaxed
        self.x_amount_tax_foot = taxes
        self.x_amount_total_foot = amount_total

    x_untaxed_amount_foot = fields.Monetary(string='Untaxed Amount', compute='_compute_amount', readonly=True)
    x_amount_tax_foot = fields.Monetary(string='Tax', readonly=True, compute='_compute_amount')
    x_amount_total_foot = fields.Monetary(string='Total', readonly=True, compute='_compute_amount')

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
    x_invoice = fields.Many2one('account.invoice')
    x_amount_untaxed = fields.Monetary(string='Amount Untaxed', related='x_invoice.amount_untaxed')
    x_taxes = fields.Monetary(string="Taxes", related="x_invoice.amount_tax")
    x_amount_total = fields.Monetary(string='Amount Total', related='x_invoice.amount_total')
    currency_id = fields.Many2one('res.currency', related='x_invoice.currency_id', store=True, readonly=True)
    is_responsible = fields.Boolean(string="Kuitansi Status", default=False)
    x_no_sjk = fields.Many2one(string="No SJK", related='x_invoice.x_no_sjk')


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    x_due_date_pembayaran = fields.Many2one('x.due.date.pembayaran')
    kuitansi_id = fields.Many2one('x.kuitansi')
    x_no_sjk = fields.Many2one('stock.picking', string="No. SJK")
    x_due_date_pembayaran = fields.Date(string="Due Date Pembayaran")
    x_tanda_terima = fields.Date(string="Tanda Terima")
    x_no_faktur = fields.Char(string="No. Faktur")
    x_sale_id = fields.Many2one('sale.order')
    x_no_po = fields.Char(string="No. PO", related='x_sale_id.x_po_cust')
    is_responsible = fields.Boolean(string="Kuitansi Status", default=False)

    # Get field PO Customer in acoount.invoice object
    # @api.onchange('partner_id')
    # def get_value_po(self):
    #     x_no_po = self.x_sale_id.x_po_cust
    #     self.x_no_po = x_no_po

    # Flagging untuk SJK ketika create invoice
    @api.multi
    def write(self, vals):
        # Update field is responsible = True
        res = super(account_invoice, self).write(vals)

        id = self.x_no_sjk
        sjk = self.env['stock.picking'].search([('id', '=', id.id)])
        sjk.write({'is_responsible': True})

        return res

    # Due Date invoice
    @api.onchange('date_invoice', 'x_tanda_terima')
    def due_date(self):
        if self.date_invoice:
            date = self.date_invoice

        date_tanda_terima = self.x_tanda_terima

        id_cus = self.partner_id
        id_cus_due_date = self.env['x.due.date.pembayaran'].search([('x_customer', '=', id_cus.id)])

        # Mengambil field yang ada pada tabel x.due.date.pembayaran
        for i in id_cus_due_date:
            customer = i.x_customer
            categ = i.x_category
            jumlah_hari = i.x_jml_hari
            type = i.x_type

            if customer:
                date_format = '%Y-%m-%d'

                # Cek apakah kategori = sjk
                if categ == 'sjk':
                    if type == 'after_sjk':
                        if jumlah_hari == '15':
                            start_date = datetime.strptime(str(date), date_format)
                            end_date = start_date + relativedelta(days=int(jumlah_hari))

                            self.x_due_date_pembayaran = end_date
                            self.date_due = end_date

                        elif jumlah_hari == '30':
                            start_date = datetime.strptime(str(date), date_format)
                            end_date = start_date + relativedelta(days=int(jumlah_hari))

                            self.x_due_date_pembayaran = end_date
                            self.date_due = end_date

                        elif jumlah_hari == '45':
                            start_date = datetime.strptime(str(date), date_format)
                            end_date = start_date + relativedelta(days=int(jumlah_hari))

                            self.x_due_date_pembayaran = end_date
                            self.date_due = end_date

                        elif jumlah_hari == '60':
                            start_date = datetime.strptime(str(date), date_format)
                            end_date = start_date + relativedelta(days=int(jumlah_hari))

                            self.x_due_date_pembayaran = end_date
                            self.date_due = end_date

                        elif jumlah_hari == '90':
                            start_date = datetime.strptime(str(date), date_format)
                            end_date = start_date + relativedelta(days=int(jumlah_hari))

                            self.x_due_date_pembayaran = end_date
                            self.date_due = end_date

                        elif jumlah_hari == '14':
                            start_date = datetime.strptime(str(date), date_format)
                            end_date = start_date + relativedelta(days=int(jumlah_hari))

                            self.x_due_date_pembayaran = end_date
                            self.date_due = end_date

                        else:
                            print "INVALID DATE!"

                    # Cek apakah tipe pembayaran sebelum sjk
                    elif type == 'before_sjk':
                        start_date = datetime.strptime(str(date), date_format)
                        if jumlah_hari == '0':
                            self.x_due_date_pembayaran = start_date
                            self.date_due = start_date

                    elif type == 'bg':
                        if jumlah_hari == '30':
                            start_date = datetime.strptime(str(date), date_format)
                            end_date = start_date + relativedelta(days=int(jumlah_hari))

                            self.x_due_date_pembayaran = end_date
                            self.date_due = end_date

                        elif jumlah_hari == '45':
                            start_date = datetime.strptime(str(date), date_format)
                            end_date = start_date + relativedelta(days=int(jumlah_hari))

                            self.x_due_date_pembayaran = end_date
                            self.date_due = end_date

                    elif type == 'dp':
                        start_date = datetime.strptime(str(date), date_format)
                        if jumlah_hari == '0':
                            self.x_due_date_pembayaran = start_date
                            self.date_due = start_date

                # Cek apakah date tanda terima tidak kosong, jika kosong maka akan lanjut pada kondisi berikutnya
                if date_tanda_terima != False:
                    if categ == 'tt':
                        if type == 'after_tt':
                            if jumlah_hari == '15':
                                start_date = datetime.strptime(str(date_tanda_terima), date_format)
                                end_date = start_date + relativedelta(days=int(jumlah_hari))

                                self.x_due_date_pembayaran = end_date
                                self.date_due = end_date

                            elif jumlah_hari == '30':
                                start_date = datetime.strptime(str(date_tanda_terima), date_format)
                                end_date = start_date + relativedelta(days=int(jumlah_hari))

                                self.x_due_date_pembayaran = end_date
                                self.date_due = end_date

                            elif jumlah_hari == '45':
                                start_date = datetime.strptime(str(date_tanda_terima), date_format)
                                end_date = start_date + relativedelta(days=int(jumlah_hari))

                                self.x_due_date_pembayaran = end_date
                                self.date_due = end_date

                            elif jumlah_hari == '60':
                                start_date = datetime.strptime(str(date_tanda_terima), date_format)
                                end_date = start_date + relativedelta(days=int(jumlah_hari))

                                self.x_due_date_pembayaran = end_date
                                self.date_due = end_date

                            elif jumlah_hari == '90':
                                start_date = datetime.strptime(str(date_tanda_terima), date_format)
                                end_date = start_date + relativedelta(days=int(jumlah_hari))

                                self.x_due_date_pembayaran = end_date
                                self.date_due = end_date

                            elif jumlah_hari == '14':
                                start_date = datetime.strptime(str(date_tanda_terima), date_format)
                                end_date = start_date + relativedelta(days=int(jumlah_hari))

                                self.x_due_date_pembayaran = end_date
                                self.date_due = end_date

                            else:
                                print "INVALID DATE!"


                elif categ == 'cod':
                    if type == 'cod':
                        start_date = datetime.strptime(str(date), date_format)
                        if jumlah_hari == '0':
                            self.x_due_date_pembayaran = start_date
                            self.date_due = start_date


    # Fungsi mengirim data pada object lain
    @api.multi
    def open_second_class(self):
        ac = self.env['ir.model.data'].xmlid_to_res_id('lpj_accounting.kuitansi_form_view', raise_if_not_found=True)
        for o in self:
            customer = o.partner_id.name

        result = {
            'name': 'Create Kuitansi',
            'view_type': 'form',
            'res_model': 'x.kuitansi',
            'view_id': ac,
            'context': {
                'default_customer': customer
            },
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'current',
        }
        return result


class stock_picking(models.Model):
    _inherit = 'stock.picking'

    is_responsible = fields.Boolean(string="SJK Status", default=False)


