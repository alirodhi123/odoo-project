# -*- coding: utf-8 -*-
import subprocess

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class mrp_production(models.Model):
     _inherit = 'mrp.production'

     x_product_bu = fields.Char(string="Product BU", compute='get_product_bu')
     x_product_label = fields.Char(compute='get_product_bu')
     x_product_laminating = fields.Char(compute='get_product_bu')
     x_product_pita = fields.Char(compute='get_product_bu')
     x_product_hot_foil = fields.Char(compute='get_product_bu')

     # REPORT
     # Get product BU yg ada di BOM dan tampilkan di report
     # Hanya BU SAJA
     @api.depends('move_raw_ids')
     def get_product_bu(self):

         product = self.env['product.product']
         for row in self.move_raw_ids:
             categ = row.product_tmpl_id.categ_id.name # Category product (BU, Label, dll)
             # Cek apakah product memiliki kategori BU
             if categ == 'BU':
                 product_bu = row.product_id.display_name  # Ambil product name dengan kategori yg telah di filter
                 self.x_product_bu = product_bu  # Mix antara kode product dengan nama product

             elif categ == 'Label':
                 product_label = row.product_id.display_name
                 self.x_product_label = product_label

             elif categ == 'Laminating 20micr':
                 product_laminating = row.product_id.display_name
                 self.x_product_laminating = product_laminating

             elif categ == 'Pita':
                 product_pita = row.product_id.display_name
                 self.x_product_pita = product_pita

             elif categ == 'Hot Foil':
                 product_hot = row.product_id.display_name
                 self.x_product_hot_foil = product_hot




