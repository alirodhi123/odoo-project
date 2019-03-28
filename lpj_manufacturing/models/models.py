# -*- coding: utf-8 -*-
import subprocess

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class mrp_production(models.Model):
     _inherit = 'mrp.production'

     def _default_id(self):
         return self.env['sale.order.line'].browse(self._context.get('active_id'))

     x_product_bu = fields.Char(string="Product BU", compute='get_product_bu')
     x_product_label = fields.Char(compute='get_product_bu')
     x_product_laminating = fields.Char(compute='get_product_bu')
     x_product_pita = fields.Char(compute='get_product_bu')
     x_product_hot_foil = fields.Char(compute='get_product_bu')
     production_id = fields.Char(string="OK Reference")
     panjang_bahan_bu_tinta = fields.Char()
     panjang_bahan_label_tinta = fields.Char()
     panjang_bahan_laminating_tinta = fields.Char()
     panjang_bahan_pita_tinta = fields.Char()
     panjang_bahan_hot_foil_tinta = fields.Char()
     panjang_bahan_max = fields.Float()
     # Untuk OK otomatis dari SO
     orderline = fields.Many2one('sale.order.line', default=_default_id)
     date_planned_start = fields.Datetime('Deadline Start', copy=False, default=fields.Datetime.now,index=True, required=True,
                          states={'confirmed': [('readonly', False)]}, oldname="date_planned", track_visibility='onchange')


     # ORDER KERJA
     # Ambil qty yg ada di SO dan letakkan di product_qty (Quantity to produce)
     # Get Product qty dari SO
     @api.onchange('x_type_mo')
     def get_qty_so(self):
         if self.x_type_mo == 'stc':
             orderline = self.orderline.id
             if orderline != False:
                 id = self.orderline.id
                 qty_so = self.env['sale.order.line'].search([('id', '=', id)])
                 # Get qty SO REAL
                 qty = qty_so.product_uom_qty
                 self.product_qty = qty


     # ORDER KERJA
     # Ambil data dari OK STICKER
     # Untuk Report OK NON STICKER
     @api.onchange('production_id')
     def get_order_kerja(self):
         id = self.production_id
         order_kerja = self.env['mrp.production'].search([('name', '=', id)])
         if order_kerja:
             bu = order_kerja.x_product_bu
             bu_label = order_kerja.x_product_label
             bu_laminating = order_kerja.x_product_laminating
             bu_pita = order_kerja.x_product_pita
             bu_hotfoil = order_kerja.x_product_hot_foil
             panjang_bahan_max = order_kerja.x_product_uom_qty

             # Pindahkan ke variabel
             self.panjang_bahan_bu_tinta = bu
             self.panjang_bahan_label_tinta = bu_label
             self.panjang_bahan_laminating_tinta = bu_laminating
             self.panjang_bahan_pita_tinta = bu_pita
             self.panjang_bahan_hot_foil_tinta = bu_hotfoil
             self.panjang_bahan_max = panjang_bahan_max


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






