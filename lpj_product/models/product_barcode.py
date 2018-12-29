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
        res.barcode = ean
        res.default_code = ean
        return res


def generate_barcode(self,vals):
    # Get parent category

    # valAtribute = vals['attribute_value_ids'][0][2]
    #
    # ukBahan = ""
    # for x in valAtribute:
    #     typAtribute = self.env['product.attribute.value']
    #     if typAtribute.attribute_id.name == 'Lebar Bahan':
    #         ukBahan = "-" + typAtribute.name


    product_tmpl_id = vals['product_tmpl_id']
    vObj = self.env['product.template'].browse(product_tmpl_id)
    # categ_id= vObj.categ_id

    seq_category = vObj.categ_id.parent_id.name

    if vObj.x_customer.x_kode_customer:
        code = vObj.x_customer.x_kode_customer # + ukBahan
    else:
        code = "" # + ukBahan

    # Get category name
    internal_category = vObj.categ_id.name

    # PRD Category
    if seq_category == 'PRD':
        prefix = "5-"
        serial_no = self.env['ir.sequence'].next_by_code('seq.prd')
        # code = self.env['res.partner'].browse(vals['x_customer']).x_kode_customer

        # jika kode customer ada
        if code != False:

            if internal_category == 'RBN':
                internal_category_val = "02"
                valDefault_code = prefix + internal_category_val + "-" + code + "-" + serial_no
                # vals['barcode'] = prefix + internal_category_val + "-" + code + "-" + serial_no

            elif internal_category == 'STC':
                internal_category_val = "01"
                valDefault_code = prefix + internal_category_val + "-" + code + "-" + serial_no
                # vals['barcode'] = prefix + internal_category_val + "-" + code + "-" + serial_no

        # jika tidak ada kode customer
        else:
            if internal_category == 'RBN':
                internal_category_val = "02"
                valDefault_code = prefix + internal_category_val + "-" + serial_no
                # vals['barcode'] = prefix + internal_category_val + "-" + serial_no

            elif internal_category == 'STC':
                internal_category_val = "01"
                valDefault_code = prefix + internal_category_val + "-" + serial_no
                # vals['barcode'] = prefix + internal_category_val + "-" + serial_no

    # MTR Category
    elif seq_category == 'MTR' or seq_category == 'All':
        serial_no_mtr = self.env['ir.sequence'].next_by_code('seq.mtr')

        # Get parts category
        if internal_category == 'Parts':
            valDefault_code = internal_category + str("-" + code or "") + "-" + serial_no_mtr
            # vals['barcode'] = internal_category + "-" + serial_no_mtr

        # Get expenses category
        elif internal_category == 'Expenses':
            serial_no_exp = self.env['ir.sequence'].next_by_code('seq.exp')

            internal_category_exp = "EXP"
            valDefault_code = internal_category_exp + str("-" + code or "") + "-" + serial_no_exp
            # vals['barcode'] = internal_category_exp + "-" + serial_no_exp

        else:
            if internal_category == 'BU':
                valDefault_code = internal_category + str("-" + code or "") + "-" + serial_no_mtr
                # vals['barcode'] = internal_category + "-" + serial_no_mtr

            elif internal_category == 'DC':
                valDefault_code = internal_category + str("-" + code or "") + "-" + serial_no_mtr
                # vals['barcode'] = internal_category + "-" + serial_no_mtr

            elif internal_category == 'TN':
                valDefault_code = internal_category + str("-" + code or "") + "-" + serial_no_mtr
                # vals['barcode'] = internal_category + "-" + serial_no_mtr

            elif internal_category == 'TN Special':
                internal_category_tns = "TNS"
                valDefault_code = internal_category_tns + str("-" + code or "") + "-" + serial_no_mtr
                # vals['barcode'] = internal_category_tns + "-" + serial_no_mtr

            elif internal_category == 'PL':
                valDefault_code = internal_category + str("-" + code or "") + "-" + serial_no_mtr
                # vals['barcode'] = internal_category + "-" + serial_no_mtr

            elif internal_category == 'TN':
                valDefault_code = internal_category + str("-" + code or "") + "-" + serial_no_mtr
                # vals['barcode'] = internal_category + "-" + serial_no_mtr

    else:
        serial_no_all = self.env['ir.sequence'].next_by_code('seq.all')

        valDefault_code = internal_category + str("-" + code or "") + "-" + serial_no_all
        # vals['barcode'] = internal_category + "-" + serial_no_all

    return  valDefault_code
