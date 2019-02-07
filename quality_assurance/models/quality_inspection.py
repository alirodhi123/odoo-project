# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from datetime import datetime

class quality_inspection(models.Model):
    _name = 'quality.inspection'

    name = fields.Char(string="No")
    x_production_id = fields.Many2one('mrp.production', required=True, string="No OK")
    x_product_id = fields.Many2one('product.product', related='x_production_id.product_id', string="Product")
    x_tanggal_inspeksi = fields.Date(default=datetime.today(), string="Tanggal Inspeksi")
    x_partner_id = fields.Many2one('res.partner', string="Customer", compute='get_customer')
    x_nama_operator = fields.Many2one('hr.employee', string="Nama Operator")
    x_nama_qc = fields.Many2one('res.users', default=lambda self: self.env.user.id, string="Created By")
    x_jumlah = fields.Float(string="Jumlah (m/pcs)")
    x_jumlah_persegi = fields.Float(string="Jumlah Meter Persegi")
    x_status_qc = fields.Selection([('hold','Hold'),('reject','Reject')], string="Status QC")
    x_deskripsi_permasalahan = fields.Text(string="Permasalahan")
    x_category_permasalahan = fields.Char(string="Category Masalah")
    x_asal_product = fields.Selection([('produksi','Produksi'),('reture','Reture Customer'),('warehouse','Warehouse')], string="Asal Product")
    x_tindakan_perbaikan = fields.Text(string="Tindakan Perbaikan")
    x_status_akhir = fields.Selection([('release', 'Release'), ('rework', 'Rework'), ('reject', 'Reject')], string="Status Akhir")
    x_jumlah_akhir = fields.Float(string="Jumlah Akhir (m/pcs)")
    x_jumlah_persegi_akhir = fields.Float(string="Jumlah Meter Persegi Akhir")


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


