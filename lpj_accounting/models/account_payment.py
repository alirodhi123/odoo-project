from odoo import models, fields, api, _
from datetime import date

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


class account_payment(models.Model):
    _inherit = 'account.payment'

    x_amount_total = fields.Monetary(compute='_amount_in_word')
    x_perkiraan_journal = fields.Char(compute='get_perkiraan_journal')
    x_nomor_journal = fields.Char(compute='get_journal_entry')
    x_draft_payment = fields.Many2one('x.register.payment', string="Draft Payment")


    # Untuk fungsi terbilang
    @api.one
    @api.depends('x_amount_total')
    def _amount_in_word(self):
        if self.amount:
            self.x_amount_total = self.amount

            self.amount_to_text = terbilang(self.x_amount_total, 'idr', 'id')


    amount_to_text = fields.Text(string="Terbilang", store=True, readonly=True,
                                 compute='_amount_in_word')


    # REPORT
    # Mengambil jurnal entry
    @api.one
    def get_journal_entry(self):
        for row in self:
            i = 0
            for o in row.move_line_ids:
                journal_entry = o.move_id
                row.x_nomor_bbk_bbm = o.move_id.name
                if i == 0 and journal_entry:
                    for journal in journal_entry:
                        nomor_journal = journal.name
                        row.x_nomor_journal = nomor_journal
                        i+=1
                        pass


    @api.one
    def get_perkiraan_journal(self):
        code = ""
        name = ""
        for o in self.move_line_ids:
            if o.full_reconcile_id:
                account_id = o.account_id

                for row in account_id:
                    code = row.code
                    name = row.name

        if code and name:
            self.x_perkiraan_journal = code + " " + name

    @api.model
    def default_get(self, fields):
        res = super(account_payment, self).default_get(fields)
        draft_payment = ""
        terms = []
        invoice_obj = self.env['account.invoice']
        invoice_ids = self.env.context.get('active_ids', False)
        invoice = invoice_obj.browse(invoice_ids)

        for row in invoice:
            draft_payment = row.x_custom_payment_id.id

        if draft_payment:
            res.update({
                'x_draft_payment': draft_payment
            })

        return res

    # Fungsi update flagging draft payment ketika sudah paid
    @api.multi
    def paid_draft_payment(self):
        draft_pay = self.x_draft_payment

        invoice_obj = self.env['x.register.payment'].search([('id', '=', draft_pay.id)])
        if invoice_obj:
            invoice_obj.write({'x_flag_paid': True})

    @api.multi
    def plafon_post(self):
        invoice = self._context.get('invoice', False)

        # FUNCTION CUSTOM ALI
        if invoice == False:
            partner_plafon = self.partner_id
            payment_type = self.payment_type
            terms = []
            values = {}
            amount_total_plafon = self.amount
            state_plafon = 'Confirm'
            name = self.name
            memo = self.communication

            # Find user input
            res_user = self.env['res.users'].search([('id', '=', self._uid)])

            partner_obj = self.env['res.partner'].search([('id', '=', partner_plafon.id)])
            if partner_obj and payment_type == 'inbound':
                values['x_date_plfn'] = date.today()
                if memo:
                    values['x_name_plfn'] = name + " " + "(" + memo + ")"
                else:
                    values['x_name_plfn'] = name
                values['x_status_plfn'] = state_plafon
                values['x_amount_plfn'] = amount_total_plafon
                values['x_user_input_plfn'] = res_user.id

                terms.append((0, 0, values))

            partner_obj.update({'x_plafon_line': terms})


    # INHERITE FUNCTION VALIDATE PAYMENT
    @api.multi
    def post(self):
        # FUNCTION UPDATE DRAFT PAYMENT
        self.paid_draft_payment()
        # PLAFON
        self.plafon_post()

        res = super(account_payment, self).post()
        return res






