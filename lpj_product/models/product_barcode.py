# -*- coding: utf-8 -*-
from odoo import api, models
import math
import re
import datetime


class ProductAutoBarcode(models.Model):
    _inherit = "product.product"

    @api.model
    def create(self, vals):
        res = super(ProductAutoBarcode, self).create(vals)
        # ean = generate_ean(str(res.id))
        ean = generate_barcode(self, vals,)
        if ean:
            res.barcode = ean
            res.default_code = ean
        return res


def generate_barcode(self,vals):
    # Get parent category

    product_tmpl_id = vals['product_tmpl_id']
    if product_tmpl_id:
        vObj = self.env['product.template'].browse(product_tmpl_id)

        # Sequence
        serial_no_mtr = self.env['ir.sequence'].next_by_code('seq.mtr')
        serial_no = self.env['ir.sequence'].next_by_code('seq.prd')
        serial_no_all = self.env['ir.sequence'].next_by_code('seq.all')

        seq_category = vObj.categ_id.parent_id.name
        kode_item = vObj.categ_id.x_kode_item
        sts_bahan_utama = vObj.categ_id.sts_bhn_utama
        internal_category = vObj.categ_id.name

        # Cek jika kode item diisi
        if kode_item:
            x_kode_item = kode_item
        else:
            x_kode_item = vObj.categ_id.id


        if vObj.x_customer.x_kode_customer:
            code = vObj.x_customer.x_kode_customer
        else:
            code = "" # + utkBahan

        # Barang Jadi
        if sts_bahan_utama.name == 'Barang Jadi':
            # jika kode customer ada
            if code:
                valDefault_code = str(x_kode_item) + "-" + code + "-" + serial_no

            # jika tidak ada kode customer
            else:
                valDefault_code = str(x_kode_item) + "-" + serial_no

        # Bahan Pembantu
        elif sts_bahan_utama.name == 'Bahan Pembantu':
            valDefault_code = str(x_kode_item) + str("-" + code or "") + "-" + serial_no_mtr

        # PLDC JADI
        elif sts_bahan_utama == 3:
            valDefault_code = str(x_kode_item) + str("-" + code or "") + "-" + serial_no_mtr

        # Tinta
        elif sts_bahan_utama.name == 'Tinta':
            valDefault_code = str(x_kode_item) + str("-" + code or "") + "-" + serial_no_mtr

        # Assets
        elif sts_bahan_utama.name == 'Assets':
            valDefault_code = str(x_kode_item) + str("-" + code or "") + "-" + serial_no_mtr

        # Expanses
        elif sts_bahan_utama.name == 'Biaya - Biaya':
            valDefault_code = str(x_kode_item) + str("-" + code or "") + "-" + serial_no_mtr

        else:
            valDefault_code = str(x_kode_item) + str("-" + code or "") + "-" + serial_no_all


        return  valDefault_code
