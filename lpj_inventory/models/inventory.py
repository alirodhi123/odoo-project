# -*- coding: utf-8 -*-
import subprocess

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class lot_barang(models.Model):
     _inherit = 'stock.picking'

     x_sj_supplier = fields.Char(string='Nomor Surat Jalan Supplier')
     x_tgl_sj_supp = fields.Datetime(string='Tanggal Surat Jalan Supplier')
     x_tgl_kedatangan_bahan = fields.Datetime(string='Tanggal Terima Bahan')


class stock_line(models.Model):
     _inherit = 'stock.pack.operation'

     keterangan = fields.Text(string="Keterangan")

