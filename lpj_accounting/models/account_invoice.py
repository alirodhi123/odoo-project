# -*- coding: utf-8 -*-

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

class account_invoice(models.Model):
    _inherit = 'account.invoice'

    # Account Invoice
    x_due_date_pembayaran_id = fields.Many2one('x.due.date.pembayaran')
    kuitansi_id = fields.Many2one('x.kuitansi')
    x_no_sjk = fields.Many2one('stock.picking', string="No. SJK")
    x_due_date_pembayaran = fields.Date(string="Due Date Pembayaran")
    x_tanda_terima = fields.Date(string="Tanda Terima Date")
    x_due_date_tt = fields.Date(string="Due Date TT")
    x_no_faktur = fields.Char(string="No. Faktur")
    x_sale_id = fields.Many2one('sale.order')
    x_no_po = fields.Char(string="No. PO", compute='get_po_cust')
    is_responsible = fields.Boolean(string="Kuitansi Status", default=False)
    x_tanggal_sjk = fields.Date(string="Tgl SJK", compute='get_tanggal_sjk')
    # Vendor Bill
    x_no_receipt = fields.Many2one('stock.picking', string="Receipt No", track_visibility='onchange')
    x_sjk_supplier = fields.Char(related='x_no_receipt.x_sj_supplier', readonly=True, string="Surat Jalan Supplier")
    x_custom_payment_id = fields.Many2one('x.register.payment', string="Draft Payment", readonly=True)

    # FOOTER
    x_discount_foot = fields.Monetary(string="Discount", compute='get_discount')
    x_bruto = fields.Monetary(string="Bruto", compute='get_discount')
    x_amount_total = fields.Monetary(compute='_amount_in_word')
    x_total_jasa = fields.Monetary(compute='get_value_jasa_material')
    x_total_material = fields.Monetary(compute='get_value_jasa_material')

    # Sql untuk no faktur tidak boleh ada yg sama
    _sql_constraints = [
        ('x_no_faktur_uniq', 'unique (x_no_faktur)', "Faktur Number already exists !"),
    ]

    # Untuk fungsi terbilang
    @api.one
    @api.depends('x_amount_total')
    def _amount_in_word(self):
        if self.amount_total:
            self.x_amount_total = self.amount_total

            self.amount_to_text = terbilang(self.x_amount_total, 'idr', 'id')

    amount_to_text = fields.Text(string="Terbilang", store=True, readonly=True,
                                 compute='_amount_in_word')


    # Flagging untuk SJK ketika create invoice
    @api.multi
    def action_invoice_open(self):
        id = self.x_no_sjk
        id_vendorbill = self.x_no_receipt

        # Customer invoice
        sjk = self.env['stock.picking'].search([('id', '=', id.id)])
        if sjk:
            sjk.write({'is_responsible': True})

        # Vendor bill
        receipt_obj = self.env['stock.picking'].search([('id', '=', id_vendorbill.id)])
        if receipt_obj:
            receipt_obj.write({'x_flag_receipt': True})

        # lots of duplicate calls to action_invoice_open, so we remove those already open
        to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
        if to_open_invoices.filtered(lambda inv: inv.state not in ['proforma2', 'draft']):
            raise UserError(_("Invoice must be in draft or Pro-forma state in order to validate it."))
        to_open_invoices.action_date_assign()
        to_open_invoices.action_move_create()
        return to_open_invoices.invoice_validate()


    # Get PO Cust
    @api.one
    def get_po_cust(self):
        # Get no SO
        so_id = self.origin
        po_cust = self.env['sale.order'].search([('name', '=', so_id)])
        for o in po_cust:
            self.x_no_po = o.x_po_cust

    # Get tanggal SJK
    @api.one
    def get_tanggal_sjk(self):

        so_id = self.x_no_sjk
        tanggal_sjk = self.env['stock.picking'].search([('id', '=', so_id.id)])
        for o in tanggal_sjk:
            self.x_tanggal_sjk = o.min_date


    # Method print invoice
    @api.multi
    def invoice_print_custom(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        self.ensure_one()
        self.sent = True
        return self.env['report'].get_action(self, 'lpj_accounting.report_invoice')


    # Due Date invoice berdasarkan TT
    @api.onchange('x_tanda_terima')
    def due_date(self):
        date_tanda_terima = self.x_tanda_terima
        if date_tanda_terima != False:
            customer =""
            id_cus_parent = self.partner_id.parent_id
            # Jika parent customer
            if id_cus_parent:
                id_cus_parent_due_date = self.env['x.due.date.pembayaran'].search([('x_customer', '=', id_cus_parent.id)])
                for row in id_cus_parent_due_date:
                    customer = row.x_customer
                    categ = row.x_category
                    jumlah_hari = row.x_jml_hari
                    type = row.x_type

            else:
                id_cus = self.partner_id
                id_cus_due_date = self.env['x.due.date.pembayaran'].search([('x_customer', '=', id_cus.id)])
                for row_row in id_cus_due_date:
                    customer = row_row.x_customer
                    categ = row_row.x_category
                    jumlah_hari = row_row.x_jml_hari
                    type = row_row.x_type

            if customer:
                date_format = '%Y-%m-%d'

                if jumlah_hari == '7':
                    start_date = datetime.strptime(str(date_tanda_terima), date_format)
                    end_date = start_date + relativedelta(days=int(jumlah_hari))

                    self.x_due_date_tt = end_date
                    self.date_due = end_date

                elif jumlah_hari == '15':
                    start_date = datetime.strptime(str(date_tanda_terima), date_format)
                    end_date = start_date + relativedelta(days=int(jumlah_hari))

                    self.x_due_date_tt = end_date
                    self.date_due = end_date

                elif jumlah_hari == '30':
                    start_date = datetime.strptime(str(date_tanda_terima), date_format)
                    end_date = start_date + relativedelta(days=int(jumlah_hari))

                    self.x_due_date_tt = end_date
                    self.date_due = end_date

                elif jumlah_hari == '45':
                    start_date = datetime.strptime(str(date_tanda_terima), date_format)
                    end_date = start_date + relativedelta(days=int(jumlah_hari))

                    self.x_due_date_tt = end_date
                    self.date_due = end_date

                elif jumlah_hari == '60':
                    start_date = datetime.strptime(str(date_tanda_terima), date_format)
                    end_date = start_date + relativedelta(days=int(jumlah_hari))

                    self.x_due_date_tt = end_date
                    self.date_due = end_date

                elif jumlah_hari == '90':
                    start_date = datetime.strptime(str(date_tanda_terima), date_format)
                    end_date = start_date + relativedelta(days=int(jumlah_hari))

                    self.x_due_date_tt = end_date
                    self.date_due = end_date

                elif jumlah_hari == '14':
                    start_date = datetime.strptime(str(date_tanda_terima), date_format)
                    end_date = start_date + relativedelta(days=int(jumlah_hari))

                    self.x_due_date_tt = end_date
                    self.date_due = end_date

                else:
                    self.x_due_date_tt = date_tanda_terima
                    self.date_due = date_tanda_terima

    # Calculate Due date pembayaran berdasarkan master due date
    @api.onchange('date_invoice', 'x_tanda_terima')
    def calculate_duedate(self):
        type_inv = self.type
        date_tanda_terima = self.x_tanda_terima
        date_sjk = self.date_invoice
        categ = ""

        if type_inv == 'out_invoice':
            id_cus_parent = self.partner_id.parent_id
            # Jika parent customer
            if id_cus_parent:
                id_cus_parent_due_date = self.env['x.due.date.pembayaran'].search([('x_customer', '=', id_cus_parent.id)])
                if id_cus_parent_due_date:
                    for row in id_cus_parent_due_date:
                        customer = row.x_customer
                        categ = row.x_category
                        jumlah_hari = row.x_jml_hari
                        type = row.x_type
                        date_format = '%Y-%m-%d'


            # Jika tidak memiliki parent customer
            else:
                id_cus = self.partner_id
                id_cus_due_date = self.env['x.due.date.pembayaran'].search([('x_customer', '=', id_cus.id)])
                if id_cus_due_date:
                    for row_row in id_cus_due_date:
                        customer = row_row.x_customer
                        categ = row_row.x_category
                        jumlah_hari = row_row.x_jml_hari
                        type = row_row.x_type
                        date_format = '%Y-%m-%d'

            # Jika berdasarkan SJK
            if categ == 'sjk' and date_sjk:
                if jumlah_hari == '7':
                    start_date = datetime.strptime(str(date_sjk), date_format)
                    end_date = start_date + relativedelta(days=int(jumlah_hari))

                    self.x_due_date_pembayaran = end_date
                    self.date_due = end_date

                elif jumlah_hari == '15':
                    start_date = datetime.strptime(str(date_sjk), date_format)
                    end_date = start_date + relativedelta(days=int(jumlah_hari))

                    self.x_due_date_pembayaran = end_date
                    self.date_due = end_date

                elif jumlah_hari == '30':
                    start_date = datetime.strptime(str(date_sjk), date_format)
                    end_date = start_date + relativedelta(days=int(jumlah_hari))

                    self.x_due_date_pembayaran = end_date
                    self.date_due = end_date

                elif jumlah_hari == '45':
                    start_date = datetime.strptime(str(date_sjk), date_format)
                    end_date = start_date + relativedelta(days=int(jumlah_hari))

                    self.x_due_date_pembayaran = end_date
                    self.date_due = end_date

                elif jumlah_hari == '60':
                    start_date = datetime.strptime(str(date_sjk), date_format)
                    end_date = start_date + relativedelta(days=int(jumlah_hari))

                    self.x_due_date_pembayaran = end_date
                    self.date_due = end_date

                elif jumlah_hari == '90':
                    start_date = datetime.strptime(str(date_sjk), date_format)
                    end_date = start_date + relativedelta(days=int(jumlah_hari))

                    self.x_due_date_pembayaran = end_date
                    self.date_due = end_date

                elif jumlah_hari == '14':
                    start_date = datetime.strptime(str(date_sjk), date_format)
                    end_date = start_date + relativedelta(days=int(jumlah_hari))

                    self.x_due_date_pembayaran = end_date
                    self.date_due = end_date

                else:
                    self.x_due_date_pembayaran = date_sjk
                    self.date_due = date_tanda_terima

            # Jika kategori TT
            elif categ == 'tt' and date_tanda_terima:
                if jumlah_hari == '7':
                    start_date = datetime.strptime(str(date_tanda_terima), date_format)
                    end_date = start_date + relativedelta(days=int(jumlah_hari))

                    self.x_due_date_pembayaran = end_date
                    self.date_due = end_date

                elif jumlah_hari == '15':
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
                    self.x_due_date_pembayaran = date_tanda_terima
                    self.date_due = date_tanda_terima

    # Fungsi mengirim data pada object lain
    @api.multi
    def open_second_class(self):
        ac = self.env['ir.model.data'].xmlid_to_res_id('lpj_accounting.kuitansi_form_view', raise_if_not_found=True)
        for o in self:
            customer = o.partner_id

        result = {
            'name': 'Create Kuitansi',
            'view_type': 'form',
            'res_model': 'x.kuitansi',
            'view_id': ac,
            'context': {
                # 'default_customer': customer
            },
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'current',
        }
        return result

    # Untuk menghitung discount yg ada di invoice
    @api.one
    def get_discount(self):
        valBruto = 0
        valDiskon = 0

        for row in self.invoice_line_ids:
            discount = row.discount

            # Menghitung Bruto
            bruto = row.quantity * row.price_unit
            valBruto += bruto
            self.x_bruto = valBruto

            # Menghitung discount invoice
            if discount:
                tempDiskon = (row.quantity * row.price_unit) * (discount / 100)
                valDiskon += tempDiskon
                self.x_discount_foot = valDiskon
                # self.x_discount_foot = valBruto - self.amount_untaxed # Bruto - untaxed amount (DPP)

    # Menghitung Harga jasa dan harga material
    @api.one
    @api.depends('invoice_line_ids.x_value_jasa', 'invoice_line_ids.x_value_material')
    def get_value_jasa_material(self):
        harga_material = 0
        harga_jasa = 0

        for row in self.invoice_line_ids:
            harga_material += row.x_value_material
            harga_jasa += row.x_value_jasa

        self.x_total_jasa = harga_jasa
        self.x_total_material = harga_material

    # Function insert bill berdasarkan WH/IN
    @api.multi
    def insert_bill(self):
        for bill in self:
            invoice_id = bill.id
            bill.delete_invoice_line_ids()
            terms = []
            integer_product_receipt = ""
            var_description = ""
            var_unit_price = ""
            var_purchase_uom = ""
            var_receipt_uom = ""
            var_factor_uom = ""

            receipt = bill.x_no_receipt

            stock_picking_obj = bill.env['stock.picking'].search([('id', '=', receipt.id)])
            if stock_picking_obj:
                procurement_group = stock_picking_obj.group_id
                for row in stock_picking_obj.pack_operation_product_ids:
                    values = {}
                    product = row.product_id
                    qty_done = row.qty_done
                    uom = row.product_uom_id
                    var_receipt_uom = row.product_uom_id.factor

                    # Purchase Order
                    if procurement_group:
                        purchase_obj = row.env['purchase.order'].search([('group_id', '=', procurement_group.id)])
                        if purchase_obj:
                            for o in purchase_obj.order_line:
                                product_po = o.product_id
                                integer_product_po = int(product_po)

                                if integer_product_receipt != integer_product_po:
                                    # Jika product po sama dengan product receipt
                                    if product_po == product:
                                        var_description = o.name
                                        var_unit_price = o.price_unit
                                        var_purchase_uom = o.product_uom.factor
                                        tax = o.taxes_id.id
                                        account_id = product_po.categ_id.property_stock_account_input_categ_id.id
                                        po_line_id = o.id

                                        # Perhitungan factor product uom
                                        var_factor_uom = (float(var_unit_price) / float(var_receipt_uom)) * float(var_purchase_uom)

                                        if product.active != False:
                                            values['invoice_id'] = invoice_id
                                            values['purchase_line_id'] = po_line_id
                                            values['product_id'] = product.id
                                            values['quantity'] = qty_done
                                            values['uom_id'] = uom.id
                                            values['account_id'] = account_id
                                            # values['invoice_line_tax_ids'] = [[6, 0, [tax]]]
                                            if var_factor_uom:
                                                values['price_unit'] = float(var_factor_uom)
                                            else:
                                                values['price_unit'] = 1

                                            if var_description:
                                                values['name'] = var_description
                                            else:
                                                values['name'] = "Tidak ada deskripsi"

                                            terms.append((0, 0, values))
                                            id_product_po = product_po
                                            integer_product_receipt = int(id_product_po)


                return self.update({'invoice_line_ids': terms})

    # Delete line function
    @api.multi
    def delete_invoice_line_ids(self):
        invoice_line_ids = []
        bill_id = self.id

        account_invoice = self.env['account.invoice'].search([('id', '=', bill_id)])
        if account_invoice:
            invoice_line_ids.append(([5]))

            return self.update({'invoice_line_ids': invoice_line_ids})




class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'

    x_harga_jasa = fields.Float(compute='get_harga_jasa_material')
    x_harga_material = fields.Float(compute='get_harga_jasa_material')
    x_qty_done_sjk = fields.Float(compute='get_qty_sjk', string="Qty done")
    x_value_jasa = fields.Float(compute='calculate_harga_jasa_material')
    x_value_material = fields.Float(compute='calculate_harga_jasa_material')
    x_price_subtotal = fields.Monetary(compute='compute_price_subtotal')
    x_price_unit_include = fields.Float(compute='compute_price_unit_include')

    # Harga jasa dan harga material
    @api.one
    def get_harga_jasa_material(self):
        product_id = self.product_id.id
        partner = self.invoice_id.partner_id
        origin = self.invoice_id.origin
        po_cus = self.invoice_id.x_no_po

        sales_order = self.env['sale.order'].search([('name', '=', origin),('partner_invoice_id', '=', partner.id),('x_po_cust', '=', po_cus)])
        if sales_order:
            for o in sales_order.order_line:
                if o.product_id == self.product_id and o.x_pecah_harga == "yes":
                    harga_jasa = o.x_harga_jasa
                    harga_material = o.x_harga_material

                    self.x_harga_jasa = harga_jasa
                    self.x_harga_material = harga_material

    # Get qty done yg ada di SJK
    @api.one
    def get_qty_sjk(self):
        partner = self.invoice_id.partner_shipping_id
        origin = self.invoice_id.origin
        id = self.invoice_id.x_no_sjk

        sjk = self.env['stock.picking'].search([('id', '=', id.id),('partner_id', '=', partner.id),('x_group_id_so', '=', origin)])
        if sjk:
            for row in sjk:
                for o in row.pack_operation_product_ids:
                    if o.product_id == self.product_id:
                        qty_done = o.qty_done
                        self.x_qty_done_sjk = qty_done

    # Calculate Harga jasa dan material
    @api.one
    def calculate_harga_jasa_material(self):

        harga_jasa = self.x_harga_jasa
        harga_material = self.x_harga_material
        qty_done = self.x_qty_done_sjk

        valHargajasa = harga_jasa * qty_done
        valHargamaterial = harga_material * qty_done

        self.x_value_jasa = valHargajasa
        self.x_value_material = valHargamaterial

    # Compute price subtotal
    @api.one
    def compute_price_subtotal(self):

        tempPrice = self.quantity * self.price_unit
        self.x_price_subtotal = tempPrice

    # Untuk mencari price unit dengan type tax include
    @api.one
    def compute_price_unit_include(self):
        price_unit = self.price_unit

        price_unit_include = price_unit / 1.1
        self.x_price_unit_include = price_unit_include










