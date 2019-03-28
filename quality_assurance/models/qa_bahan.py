# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class qa_alert(models.Model):
     _inherit = 'quality.alert'

     qa_id = fields.One2many('x.qa.bahan', 'x_qa', copy=True)
     x_nomor_lot = fields.Char('Nomor Lot', track_visibility='onchange')
     x_ukuran = fields.Char('Ukuran', track_visibility='onchange')
     x_jenis = fields.Selection([('bahan','Bahan'),('tinta','Tinta'), ('product','Product'),('plate','Plate'),('diecut','Diecut')],
                                string = 'Jenis Produk')


class qa_bahan(models.Model):
     _name = 'x.qa.bahan'
     x_qa = fields.Many2one('quality.alert', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)

     # x_nama_bahan = fields.Selection([('gtop', 'Grammature Top'), ('grel', 'Grammature Release')], string='Pengujian')

     x_waktu_qa_bahan = fields.Datetime(string='Waktu QA Bahan', readonly=True, default=lambda self: fields.datetime.now())
     x_user_qa_bahan = fields.Many2one('res.users', 'User QA Tinta', readonly=True, default=lambda self: self.env.user)

     x_ukuran = fields.Char(string='Ukuran Bahan')
     x_grammatur_top = fields.Char(string='Grammature Top (gsm)')
     x_grammatur_release = fields.Char(string='Grammature Release (gsm)')
     x_thickness_top = fields.Char(string='Thickness Top (u)')
     x_thickness_release = fields.Char(string='Thickness Release (u)')
     x_tdk_gelombang = fields.Selection([('1', 'Approve'), ('0', 'Reject')], string='Bahan Tidak Bergelombang')
     x_tdk_ngelokor = fields.Selection([('1', 'Approve'), ('0', 'Reject')], string='Bahan Tidak Ngelokor')
     x_tdk_gembos = fields.Selection([('1', 'Approve'), ('0', 'Reject')], string='Bahan Tidak Gembos')
     x_tdk_penyok = fields.Selection([('1', 'Approve'), ('0', 'Reject')], string='Core Tidak Penyok')

