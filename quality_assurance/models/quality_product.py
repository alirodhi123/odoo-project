# -*- coding: utf-8 -*-

from odoo import api, fields, models


class qa_cetak_product(models.Model):
    _inherit = 'quality.alert'
    _name = 'quality.alert'

    x_qa_cetak_lines = fields.One2many('x.qa.cetak.lines', 'x_qa_alert_id', string='QA Cetak')
    x_qa_hotprint_lines = fields.One2many('x.qa.hotprint.lines', 'x_qa_alert_id', string='QA Cetak')
    x_qa_laminating_product_lines = fields.One2many('x.qa.laminating.lines', 'x_qa_alert_id', string='QA Laminating')
    x_qa_varnish_product_lines = fields.One2many('x.qa.varnish.lines', 'x_qa_alert_id', string='QA Varnish')
    x_qa_plongdiecut_product_lines = fields.One2many('x.qa.plongdiecut.lines', 'x_qa_alert_id',
                                                     string='QA Plong / Diecut')
    x_qa_slitingsheeting_product_lines = fields.One2many('x.qa.slitingsheeting.lines', 'x_qa_alert_id',
                                                         string='QA Slitting / Sheeting')
    x_qa_packing_product_lines = fields.One2many('x.qa.packing.lines', 'x_qa_alert_id',
                                                 string='QA Packing')


class qa_cetak_product_lines(models.Model):
    _name = 'x.qa.cetak.lines'
    x_qa_alert_id = fields.Many2one('quality.alert')
    x_qa_artwork = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Gb. Sesuai Artwork')
    x_qa_text = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Text Sesuai Artwork')
    x_qa_warna_std = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Warna Sesuai Std')
    x_qa_warna_cetakan = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Warna Cetakan Rata')
    x_qa_kotor = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Tidak Kotor')
    x_qa_jembret = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Tidak Jembret')
    x_qa_inspection = fields.Integer('Quality Inspection (m)')


class qa_hotprint_product_lines(models.Model):
    _name = 'x.qa.hotprint.lines'
    x_qa_alert_id = fields.Many2one('quality.alert')
    x_qa_warnafoil = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Warna Foil Sesuai')
    x_qa_kerataanfoil = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Kerataan Foil Sesuai')
    x_qa_ketepatanposisi = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Ketepatan Posisi Sesuai')
    x_qa_tidakmenembusrelease = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Tidak Menembus Release')
    x_qa_tidakrontok = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Tidak Rontok')


class qa_laminating_product_lines(models.Model):
    _name = 'x.qa.laminating.lines'
    x_qa_alert_id = fields.Many2one('quality.alert')
    x_qa_kerataanpermukaan = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Kerataan Permukaan Sesuai')
    x_qa_tidakbergelembung = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Tidak Bergelembung')
    x_qa_tidakkotor = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Tidak Kotor')


class qa_varnish_product_lines(models.Model):
    _name = 'x.qa.varnish.lines'
    x_qa_alert_id = fields.Many2one('quality.alert')
    x_qa_kerataanpermukaanvarnish = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')],
                                                     string='Kerataan Permukaan Varnish Sesuai')
    x_qa_efekvarnish = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Evek Varnish')


class qa_plongdiecut_product_lines(models.Model):
    _name = 'x.qa.plongdiecut.lines'
    x_qa_alert_id = fields.Many2one('quality.alert')
    x_qa_dimensi = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Dimensi Sesuai')
    x_qa_posisi = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Posisi Sesuai')
    x_qa_perforasi = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Perforasi Sesuai')
    x_qa_stickertembus = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Sticker Tembus')
    x_qa_releasetidakmenembus = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Release Tidak Menembus')


class qa_slitingsheeting_product_lines(models.Model):
    _name = 'x.qa.slitingsheeting.lines'
    x_qa_alert_id = fields.Many2one('quality.alert')
    x_qa_arahroll = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8')],
        string='Arah Roll')
    x_qa_panjangroll = fields.Integer(string='Panjang Roll(M)')
    x_qa_ketebalancore = fields.Integer(string='Ketebalan Core(M)')
    x_qa_outerdiameter = fields.Integer(string='Outer Diameter(cm)')
    x_qa_ketepatanposisi = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Ketepatan Posisi Sesuai')
    x_qa_finalcheck = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Final Check Sesuai')


class qa_packing_product_lines(models.Model):
    _name = 'x.qa.packing.lines'
    x_qa_alert_id = fields.Many2one('quality.alert')
    x_qa_jumlahperpack = fields.Integer(string='Jumlah Per Pack')
    x_qa_identitaspacking = fields.Selection([('1', 'Sesuai'), ('0', 'Tidak Sesuai')], string='Identitas Packing Sesuai')
