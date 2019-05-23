# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Pembayaran(models.Model):
    _name = 'x.due.date.pembayaran'

    x_invoice = fields.Many2one('account.invoice')
    x_customer = fields.Many2one('res.partner', string="Customer")
    x_lama_pembayaran = fields.Text(string="Lama Pembayaran")
    x_keterangan = fields.Text(string="Keterangan")
    x_jml_hari = fields.Selection(string="Jumlah Hari", selection = [('7', '7 Hari'),
                                                                     ('15', '15 Hari'),
                                                                     ('30', '30 Hari'),
                                                                     ('45', '45 Hari'),
                                                                     ('60', '60 Hari'),
                                                                     ('90', '90 Hari'),
                                                                     ('14', '14 Hari'),
                                                                     ('0', 'On Day')])
    x_category = fields.Selection(string="Kategori Pembayaran", selection = [('sjk', 'SJK'),
                                                                             ('tt', 'TT'),
                                                                             ('cod', 'COD')])
    x_type = fields.Selection(string="Type Pembayaran", selection = [('after_sjk', 'Pelunasan Setelah SJK'),
                                                                     ('after_tt', 'Pelunasan Setelah TT'),
                                                                     ('before_sjk', 'Pelunasan Sebelum SJK'),
                                                                     ('bg', 'BG Mundur'),
                                                                     ('cod', 'COD'),
                                                                     ('dp', 'DP')])

