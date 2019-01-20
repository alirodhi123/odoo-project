# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools import amount_to_text_en, datetime, timedelta
from odoo.tools import amount_to_text
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    x_due_date_pembayaran_id = fields.Many2one('x.due.date.pembayaran')
    kuitansi_id = fields.Many2one('x.kuitansi')
    x_no_sjk = fields.Many2one('stock.picking', string="No. SJK")
    x_due_date_pembayaran = fields.Date(string="Due Date Pembayaran")
    x_tanda_terima = fields.Date(string="Tanda Terima Date")
    x_no_faktur = fields.Char(string="No. Faktur")
    x_sale_id = fields.Many2one('sale.order')
    x_no_po = fields.Char(string="No. PO", compute='get_po_cust')
    is_responsible = fields.Boolean(string="Kuitansi Status", default=False)
    x_tanggal_sjk = fields.Date(string="Tgl SJK", compute='get_tanggal_sjk')

    # FOOTER INVOICE
    x_diskon = fields.Monetary(string="Diskon")
    x_dpp = fields.Monetary(string="DPP", readonly=True, compute='get_amount_total')
    x_amount_taxx = fields.Monetary(string="Tax", readonly=True, compute='get_amount_total')
    x_amount_total = fields.Monetary(string="Total", readonly=True, compute='get_amount_total')
    x_residual = fields.Monetary(string="Amount Due", readonly=True, compute='get_amount_total')


    # Flagging untuk SJK ketika create invoice
    @api.multi
    def write(self, vals):
        # Update field is responsible = True
        res = super(account_invoice, self).write(vals)

        id = self.x_no_sjk
        sjk = self.env['stock.picking'].search([('id', '=', id.id)])
        sjk.write({'is_responsible': True})

        return res

    # Get PO Cust
    @api.one
    def get_po_cust(self):
        # Get no SO
        so_id = self.origin
        po_cust = self.env['sale.order'].search([('name', '=', so_id)])
        for o in po_cust:
            self.x_no_po = o.x_po_cust

    # Get tanggal pengiriman di SJK
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

    @api.depends('x_diskon')
    def get_amount_total(self):
        bruto = self.amount_untaxed
        diskon = self.x_diskon
        dpp = self.x_dpp

        if diskon != 0:
            dpp = bruto - diskon
            # Perhitungan Tax
            amount_tax = (dpp * 10) / 100

            self.x_dpp = dpp
            self.x_amount_taxx = amount_tax
            self.x_amount_total = dpp + amount_tax
            self.x_residual = self.x_amount_total
        else:
            self._compute_amount()








