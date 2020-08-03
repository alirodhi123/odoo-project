# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from datetime import datetime

class quality_inspection(models.Model):
    _name = 'quality.inspection'

    quality_inspection_ids = fields.One2many('quality.inspection.line', 'quality_inspection_id', string="Quality Inspection Line")
    name = fields.Char(string="No")
    x_production_id = fields.Many2one('mrp.production', required=True, string="No OK")
    x_product_id = fields.Many2one('product.product', related='x_production_id.product_id', string="Product")
    # x_type_product = fields.Char(compute='get_type_mo', string="Product Type")
    x_type_product = fields.Selection([('stc', 'Sticker'), ('ink', 'Tinta Campuran'), ('plate', 'Plate'),('diecut', 'Diecut')],
                                      string="Product Type")
    x_partner_id = fields.Many2one('res.partner', string="Customer", compute='get_customer')
    x_nama_qc = fields.Many2one('res.users', default=lambda self: self.env.user.id, string="Created By", readonly=True)
    x_jumlah_foot = fields.Float(string="Total Qty Akhir", compute='compute_footer')
    x_jumlah_persegi_foot = fields.Float(string="Total Qty Meter Persegi Akhir", compute='compute_footer')
    x_jumlah_awal_foot = fields.Float(string="Total Qty Awal", compute='compute_footer')
    x_jumlah_awal_persegi_foot = fields.Float(string="Total Qty Awal Persegi", compute='compute_footer')
    x_keterangan = fields.Text(string="Keterangan")
    state = fields.Selection(
        [('1', 'Open'), ('2', 'Identifikasi'), ('3', 'Rework'), ('4', 'Follow Up'),
         ('5', 'Done')], default='1')

    # field line pindah ke header
    x_category_permasalahan_baru = fields.Many2one('problem.tags', string="Category Masalah")
    x_deskripsi_permasalahan = fields.Text(string="Deskripsi")
    x_name_issue = fields.Text(string='Nama Issue', store=True, readonly=True)
    x_repeat = fields.Boolean(string='Repeat')
    x_tanggal_inspeksi = fields.Date(string="Tanggal Inspeksi")
    x_mesin = fields.Many2many('x.mesin.tags', string="Type Mesin")
    x_asal_product = fields.Selection([('produksi', 'Produksi'),
                                       ('reture', 'Reture Customer'),
                                       ('warehouse', 'Warehouse')], string="Asal Product")
    x_status_qc = fields.Selection([('hold', 'Hold'), ('reject', 'Reject')], string="Status QC")
    x_nama_operator = fields.Many2one('hr.employee', string="Nama Operator")
    x_tindakan_perbaikan = fields.Text(string="Tindakan Perbaikan")
    x_status_akhir = fields.Selection([('release', 'Release'), ('rework', 'Rework'), ('reject', 'Reject')],
                                      string="Status Akhir")
    image = fields.Binary(string="Gmbr Defect")
    x_department = fields.Many2one('hr.department', string='Department')

    @api.onchange('x_category_permasalahan_baru')
    def nama_issue(self):
        if self.x_partner_id:
            if self.x_category_permasalahan_baru:
                self.x_name_issue = self.x_partner_id.name + ' - ' + self.x_category_permasalahan_baru.name
            else:
                self.x_name_issue = self.x_partner_id.name + ' - '
        else:
            if self.x_category_permasalahan_baru:
                self.x_name_issue = ' - ' + self.x_category_permasalahan_baru.name
            else:
                self.x_name_issue = ' - '


    @api.multi
    def action_next(self):
        new_state = int(self.state) + 1
        self.state = str(new_state)
        self.color = 3

    @api.multi
    def action_prev(self):
        new_state = int(self.state) - 1
        self.state = str(new_state)
        self.color = 3


    # Sequence
    @api.model
    def create(self, vals):
        res = super(quality_inspection, self).create(vals)

        sequence = self.env['ir.sequence'].next_by_code('sequence.quality.inspection') or ('New')
        res.update({'name': sequence})

        return res


    # Get customer dari SO yang ada di OK
    @api.one
    def get_customer(self):
        id = self.x_production_id
        manufacturing = self.env['mrp.production'].search([('id', '=', id.id)])
        if manufacturing:
            for sale_order in manufacturing:
                for row in sale_order.order:
                    customer = row.partner_id
                    self.x_partner_id = customer

    # Get type MO
    @api.onchange('x_production_id')
    def get_type_mo(self):
        id = self.x_production_id
        manufacturing = self.env['mrp.production'].search([('id', '=', id.id)])
        if manufacturing:
            for mrp in manufacturing:
                type_mo = mrp.x_type_mo
                if type_mo == 'stc':
                    self.x_type_product = 'stc'
                elif type_mo == 'ink':
                    self.x_type_product = 'ink'
                elif type_mo == 'plate':
                    self.x_type_product = 'plate'
                else:
                    self.x_type_product = 'diecut'

    # FOOTER CALCULATE
    # Perhitungan jumlah meter di footer
    @api.one
    def compute_footer(self):
        jumlah = 0
        jumlah_persegi = 0
        jumlah_awal = 0
        jumlah_awal_persegi = 0

        for row in self.quality_inspection_ids:
            jumlah_awal += row.x_jumlah_awal
            jumlah_awal_persegi += row.x_jumlah_persegi_awal
            jumlah += row.x_jumlah
            jumlah_persegi += row.x_jumlah_persegi

        self.x_jumlah_awal_foot = jumlah_awal
        self.x_jumlah_awal_persegi_foot = jumlah_awal_persegi
        self.x_jumlah_foot = jumlah
        self.x_jumlah_persegi_foot = jumlah_persegi



class quality_inspection_line(models.Model):
    _name = 'quality.inspection.line'

    quality_inspection_id = fields.Many2one('quality.inspection', ondelete='cascade')
    x_deskripsi_permasalahan = fields.Text(string="Deskripsi")
    x_category_permasalahan = fields.Many2many('problem.tags', string="Category Masalah")
    x_category_permasalahan_baru = fields.Many2one('problem.tags', string="Category Masalah")
    x_asal_product = fields.Selection([('produksi', 'Produksi'),
                                       ('reture', 'Reture Customer'),
                                       ('warehouse', 'Warehouse')], string="Asal Product")
    x_tindakan_perbaikan = fields.Text(string="Tindakan Perbaikan")
    x_status_akhir = fields.Selection([('release', 'Release'), ('rework', 'Rework'), ('reject', 'Reject')],string="Status Akhir")
    x_jumlah = fields.Float(string="Qty Akhir(m/pcs)")
    x_jumlah_persegi = fields.Float(string="Qty Akhir(m2)", compute='calculate_meter_persegi')
    x_jumlah_awal = fields.Float(string="Qty Awal(m/pcs)")
    x_jumlah_persegi_awal = fields.Float(string="Qty Awal(m2)", compute='calculate_meter_persegi')
    x_status_qc = fields.Selection([('hold', 'Hold'), ('reject', 'Reject')], string="Status QC")
    x_nama_operator = fields.Many2one('hr.employee', string="Nama Operator")
    x_tanggal_inspeksi = fields.Date(default=datetime.today(), string="Tanggal Inspeksi")
    image = fields.Binary(string="Gmbr Defect")
    second_image = fields.Binary(string="Gmbr Keseluruhan")
    x_mesin = fields.Many2many('x.mesin.tags', string="Type Mesin")
    x_department = fields.Many2one('hr.department', string='Department')
    x_name_issue = fields.Text(string='Nama Issue', store=True)
    x_repeat = fields.Boolean(string='Repeat')

    @api.onchange('x_category_permasalahan_baru')
    def nama_issue(self):
        if self.x_category_permasalahan_baru:
            self.x_name_issue = self.quality_inspection_id.x_partner_id.name + ' - ' + self.x_category_permasalahan_baru.name
        else:
            self.x_name_issue = self.quality_inspection_id.x_partner_id.name + ' - '

    # METER PERSEGI Akhir
    # Rumus mencari meter persegi
    # m2 = (lebar barang * panjang barang * qty) / 0.8
    @api.one
    def calculate_meter_persegi(self):
        id = self.quality_inspection_id.x_product_id
        qty_akhir = self.x_jumlah
        qty_awal = self.x_jumlah_awal

        product_product = self.env['product.product'].search([('id', '=', id.id)])
        if product_product:
            for o in product_product:
                lebar_barang = o.x_width / 1000 # (Konversi mm ke m)
                panjang_barang = o.x_length / 1000 # (Konversi mm ke m)

            # Rumus Meter Persegi Awal
            meter_persegi_awal = (lebar_barang * panjang_barang * qty_awal) / 0.8
            self.x_jumlah_persegi_awal = meter_persegi_awal

            # Rumus Meter Persegi Akhir
            meter_persegi = (lebar_barang * panjang_barang * qty_akhir) / 0.8
            self.x_jumlah_persegi = meter_persegi

        return True

