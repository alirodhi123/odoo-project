# -*- coding: utf-8 -*-
import subprocess

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp
from datetime import date
from dateutil.relativedelta import relativedelta
from datetime import datetime, time

class sq(models.Model):
    _inherit = 'x.cusrequirement'
    x_so_line= fields.One2many('sale.order.line', 'x_customer_requirement', string='hub SQ ke SO line')


class minmax_mo(models.Model):
     _inherit = 'mrp.production'

     # Untuk mengambil product order line berdasarkan trigger dari button open SO
     def _default_id(self):
         return self.env['sale.order.line'].browse(self._context.get('active_id'))

     # uswa-tambah selection 'trial dan buffer'
     x_type_mo = fields.Selection([('stc', 'Sticker'), ('ink', 'Tinta Campuran'), ('plate', 'Plate'),('diecut', 'Diecut'),('trial', 'Trial'),('buffer', 'Buffer')], string='Type MO', required=True)
     # customer = fields.Many2one('res.partner', string='Customer', related = 'order.partner_id')
     customer_code = fields.Char(string="Kode Customer", compute='get_kode_customer')
     categ_id = fields.Many2one(readonly = True, related = 'product_id.product_tmpl_id.categ_id')
     jml_lot = fields.Char(string='Jumlah Lot')
     x_kode_awal = fields.Char(string='Kode Awal')
     x_kode_akhir = fields.Char(string='Kode Akhir')
     jml_print = fields.Char(string='Jumlah Print', default=2)
     x_type_print = fields.Selection([('all', 'All'), ('specific', 'Specific')], string='Type Print out', default = 'all')
     x_keterangan = fields.Text(string="Keterangan")
     x_width = fields.Float(string="Width", compute='get_value')
     quantity_so = fields.Float(string="Quantity SO", compute='get_value_qty_so')
     x_qty_per_lot = fields.Float(string="Qty per Lot")
     x_berat_per_lot = fields.Float(string="Berat per Lot", compute='gram_per_lot')
     x_tipe_packing_ok = fields.Selection([('roll', 'Roll'), ('sheet', 'Sheet'), ('fanfold ', 'Fan Fold')],
                                       track_visibility='onchange', string='Type Packing', related='product_id.x_type_packing', readonly=True)
     x_pcs_units_ok = fields.Float(string='Pcs per Roll/Sheet/Fold', track_visibility='onchange', related='product_id.x_pcs_units', readonly=True)
     x_packing_box_ok = fields.Float(string='Pack/Fold per Box', track_visibility='onchange', related='product_id.x_packing_box', readonly=True)


     # Untuk OK otomatis parsing value dari open SO (SQ)
     # POP MESSAGE OK
     order = fields.Many2one('sale.order', string='Kode SO')
     # x_duedate_so = fields.Datetime(string = 'Duedate kirim SO', compute = 'duedate_kirim')
     x_product_order_line = fields.Many2one('sale.order.line', default=_default_id)
     x_flag = fields.Boolean()
     x_due_kirim = fields.Datetime(string="Due Date Kirim", readonly=True)
     x_toleransi = fields.Float(string='Toleransi SO')
     x_note_so = fields.Text(string="Notes SO", readonly=True)
     x_customer_so = fields.Many2one('res.partner', related='order.partner_id', string="Customer", readonly=True)

     # Pcs to meter khusus untuk roll
     x_pcs_units = fields.Float(string="Roll/sheet/fold", compute='get_value')
     x_jarak_druk = fields.Float(string="Jarak Druk", compute='get_value')
     pcs_to_meter = fields.Float(string="Hasil konversi", compute='convert_pcs_to_meter')

     # Perhitungan QTY MAX
     x_quantity_max = fields.Integer(string='Quantity Maksimal', compute='compute_max_qty')
     x_isi_druk = fields.Integer(compute='get_layout_product')
     x_jarak_druk_product = fields.Float(compute='get_layout_product')

     # Untuk Jumlah druk MIN & MAX
     x_across_number = fields.Integer(compute='get_jumlah_druk')
     x_arround_number = fields.Integer(compute='get_jumlah_druk')
     jumlah_druk_min = fields.Float(compute='calculate_jumlah_druk')
     jumlah_druk_max = fields.Float(compute='calculate_jumlah_druk')
     x_across_druk = fields.Float(compute='get_druk')
     x_arround_druk = fields.Float(compute='get_druk')

     # Konversi Pcs ke gram
     x_gram_stc = fields.Float(string='Berat Stc', store=True, compute='calculate_pcs_to_gram')
     x_gram_per_pcs = fields.Float(string='Berat per Pcs', compute='berat_per_pcs')

     # Print lot
     x_flag_print_lot = fields.Boolean(string="Flag Print Lot", default=False)
     x_flag_tgl_print_lot = fields.Date(string="Tanggal Print Lot", readonly=True)

     # uswa-tambah field untuk nampung format barcode ok dan expnya
     # x_format_barcode = fields.Char(string='format barcode')
     # x_expdate_barcode = fields.Datetime(string='exp barcode')


     # ORDER KERJA
     # Ubah product sesuai dengan product yang ada di order line (Berdasarkan Open SO yang di klik
     # Onchange product
     @api.onchange('x_type_mo')
     def set_value(self):
          product_order_line = self.x_product_order_line
          type_mo = self.x_type_mo

          if type_mo == 'stc':
               # Jika product yang ada di order line (SQ) kosong
               if product_order_line.id == False:
                    self.product_id = self.product_id
               else:
                    product = product_order_line.product_id
                    self.product_id = product

     # ORDER KERJA
     # Ambil qty yg ada di SO dan letakkan di product_qty (Quantity to produce)
     # Get Product qty dari SO
     @api.onchange('x_type_mo')
     def get_qty_so(self):
          for manufacturing in self:
               if manufacturing.x_type_mo == 'stc':
                    product_order_line = manufacturing.x_product_order_line.id
                    if product_order_line != False:
                         id = manufacturing.x_product_order_line.id

                         sale_order_line = manufacturing.env['sale.order.line'].search([('id', '=', id)])
                         if sale_order_line:
                              for row in sale_order_line:
                                   qty_ordered = row.product_uom_qty
                                   qty_produced = row.x_qty_produced_ok

                                   if qty_produced == 0.0:
                                        # Get qty SO REAL
                                        qty = qty_ordered
                                        manufacturing.product_qty = qty
                                   else:
                                        # Jika qty produced != 0, maka yang diambil adalah qty terakhir dari qty produced
                                        # Mencari sisa qty yang harus di produksi
                                        selisih = qty_ordered - qty_produced
                                        manufacturing.product_qty = selisih


     @api.multi
     def action_next(self):
          flag_print_lot = self.x_flag_print_lot

          # Jika belum pernah di print
          if flag_print_lot == False:
               self.x_flag_print_lot = True
               self.x_flag_tgl_print_lot = date.today()

          return {
               'name': 'Go to website',
               'res_model': 'ir.actions.act_url',
               'type': 'ir.actions.act_url',
               'url': 'http://192.168.1.8:8086/lot/production/lot_barang?id=1&jumlah=' + self.jml_lot + '&awal=' + str(self.x_kode_awal) + '&akhir=' + str(self.x_kode_akhir) + '&name=' + self.name + '&print=' + self.jml_print + '&categ=' + str(self.categ_id.name)+ '&cus=' + str(self.customer_code)+'&date=' + self.date_planned_start+'&qtyakhir=False'
               # 'url': 'http://192.168.2.40:8086/world.php?jumlah='+ self.jml_lot
               # 'url': 'http://192.168.1.8:8081/Lot?id=1&jumlah=' + self.jml_lot +'&name='+ self.name
          }

# uswa-tambah fungsi ini untuk print barcose via odoo di ok
     @api.multi
     def action_print_barcode_ok(self):
          flag_print_lot = self.x_flag_print_lot

          self.jml_lot
          self.x_kode_awal
          self.x_kode_akhir
          self.name
          self.jml_print
          self.categ_id.name
          self.customer_code
          self.date_planned_start

          # Jika belum pernah di print
          if flag_print_lot == False:
               self.x_flag_print_lot = True
               self.x_flag_tgl_print_lot = date.today()


          jml_lotsj = self.jml_lot
          tgl_planned = self.date_planned_start

          if jml_lotsj > 0:
               temp = self.name
               ok = temp.split('-')[2]

          if tgl_planned:
               date_format = "%Y-%m-%d %H:%M:%S"
               six_months_after = datetime.strptime(str(tgl_planned), date_format) + relativedelta(months=6)
               self.x_expdate_barcode = six_months_after

               mth_exp = six_months_after
               temp = mth_exp.month

               self.x_format_barcode = ok+temp


          return self.env['report'].get_action(self, 'lpj_manufacturing.report_generate_barcode_ok')



     # Get one2many x_layout_product_ids (REPORT)
     @api.one
     def get_value(self):
          id = self.product_id.id
          accros = self.env['product.product'].search([('id', '=', id)])
          type_packing = accros.x_type_packing

          # Cek apakah type packing = Roll
          if type_packing == "roll":
               nilai = accros.x_pcs_units
               self.x_pcs_units = nilai

          for o in accros.x_layout_product_ids:
               type = o.x_type
               variable = o.x_jumlah
               jarak_druk = o.x_druk

               if type == "across" or type == "acrossdigital":
                    self.x_width = variable

               # get value arround (REPORT)
               elif type == "arround" or type == "arrounddigital":
                    self.x_jarak_druk = jarak_druk  # Satuan mm


     # Get one2many order_line qty SO (REPORT)
     @api.depends('product_id', 'x_toleransi')
     def get_value_qty_so(self):
          for row in self:
               toleransi_so = row.x_toleransi
               id = row.order.id
               qty_so = row.env['sale.order'].search([('id', '=', id)])
               for o in qty_so.order_line:
                    if row.product_id == o.product_id:
                         # Get qty SO REAL
                         qty = o.product_uom_qty
                         # Menghitung TOLERANSI + QTY SO REAL
                         valToleransi = ((toleransi_so / 100) * qty) # (5/100) : 20000 = 1000
                         valQtyFix = valToleransi + qty # Hasil toleransi + qty SO REAL (1000 + 20000)
                         # Put in new variable
                         row.quantity_so = valQtyFix

     # Convert pcs to meter untuk REPORT OK
     @api.depends('x_jarak_druk', 'x_pcs_units')
     def convert_pcs_to_meter(self):
          for row in self:
               hasil = row.x_pcs_units * row.x_jarak_druk #Masih dalam mm
               row.pcs_to_meter = hasil / 1000 # Convert hasil (mm) ke meter


     # MAX QTY MO
     # Ambil jarak dan isi druk untuk perhitungan QTY MAX
     @api.one
     def get_layout_product(self):
          id = self.product_id.id
          product = self.env['product.product'].search([('id', '=', id)])
          for o in product.x_layout_product_ids:
               type = o.x_type
               jarak_druk = o.x_druk
               isi_druk = o.x_number
               # Jika type product accross maka ambil isi druk
               if type == "across" or type == "acrossdigital":
                    self.x_isi_druk = isi_druk # Get isi druk dari accross
               else:
                    self.x_jarak_druk_product = jarak_druk # Get jarak druk dari arround


     # PERHITUNGAN QTY MAX
     # Qty max berdasarkan stock yang ada di gudang gudang
     # REPORT
     @api.depends('quantity_so', 'x_toleransi', 'product_qty', 'x_product_uom_qty', 'x_isi_druk', 'x_jarak_druk_product')
     def compute_max_qty(self):
          for manufacturing in self:
               qty_so = manufacturing.quantity_so
               toleransi_so = manufacturing.x_toleransi
               qty_to_produce = manufacturing.product_qty
               isi_druk = manufacturing.x_isi_druk
               jarak_druk = manufacturing.x_jarak_druk_product / 10 #konversi mm ke cm
               panjang_bahan_max = manufacturing.x_product_uom_qty

               if jarak_druk != 0:
                    qty_max_temp = (panjang_bahan_max * isi_druk) / jarak_druk
                    qty_max = qty_max_temp * 100
                    manufacturing.x_quantity_max = qty_max


     # REPORT JUMLAH DRUK
     # Get jumlah druk MAX dan jumlah druk MIN dari product
     # Model Product.product
     @api.one
     def get_jumlah_druk(self):
          self.ensure_one()
          id = self.product_id.id
          product_product = self.env['product.product'].search([('id', '=', id)])
          if product_product:
               for row in product_product.x_layout_plong_ids:
                    if row.x_plong_type == 'across' or row.x_plong_type == 'acrossdigital':
                         across_number = row.x_plong_number
                         self.x_across_number = across_number
                    else:
                         arround_number = row.x_plong_number
                         self.x_arround_number = arround_number


     # PERHITUNGAN JUMLAH DRUK MAX DAN MINIMAL
     # Ambil dari fungsi get_jumlah_druk
     @api.depends('product_qty', 'x_quantity_max', 'x_across_number', 'x_arround_number')
     def calculate_jumlah_druk(self):
          for row in self:
               qty_to_produce = row.product_qty
               qty_max = row.x_quantity_max
               var_across_number = row.x_across_number
               var_arround_number = row.x_arround_number

               if var_across_number != 0 and var_arround_number != 0:
                    druk_min = qty_to_produce / (var_across_number * var_arround_number)
                    druk_max = qty_max / (var_across_number * var_arround_number)
                    row.jumlah_druk_min = druk_min
                    row.jumlah_druk_max = druk_max

     # Get kode customer SO
     # Untuk PRINT NO LOT
     @api.one
     def get_kode_customer(self):
          for data in self:
               sale_order = data.order

               if sale_order:
                    for row in sale_order:
                         customer = row.partner_id
                         if customer:
                              for o in customer:
                                   kode_customer = o.x_kode_customer
                                   if kode_customer:
                                        data.customer_code = kode_customer
                                   pass

     # Untuk mendapatkan druk across dan arround
     @api.one
     def get_druk(self):
          # Product product
          for product in self.product_id:
               for line in product.x_layout_product_ids:
                    type = line.x_type
                    if type == 'arround' or type == 'arrounddigital':
                         size_arround = line.x_size
                         space_arround = line.x_space
                         self.x_arround_druk = size_arround + space_arround

                    else:
                         size_across = line.x_size
                         space_across = line.x_space
                         self.x_across_druk = size_across + space_across

     # Hitung berat sticker
     @api.depends('product_qty')
     def calculate_pcs_to_gram(self):
          qty_to_produce = self.product_qty
          across_number = self.x_across_number
          arround_number = self.x_arround_number
          across_druk = self.x_across_druk
          arround_druk = self.x_arround_druk
          std_afalan_arround = 0
          std_afalan_across = 0

          if self.x_type_mo == 'stc':
               for product in self.product_id:
                    for line in product.x_layout_product_ids:
                         type = line.x_type
                         if type == 'arround' or type == 'arrounddigital':
                              std_afalan_arround += line.x_std_afalan
                              ref_lebaran_arround =  (arround_number * arround_druk) + std_afalan_arround

                         else:
                              std_afalan_across += line.x_std_afalan
                              ref_lebaran_across = (across_number * across_druk) + std_afalan_across

               # Get lebaran bahan OK (jika sudah ada move raw ids)
               if self.move_raw_ids:
                    for row in self.move_raw_ids:
                         categ_product = row.product_id.categ_id.sts_bhn_utama.name
                         if categ_product == 'Bahan Utama':
                              bahan_utama_mm = row.product_id.x_variant_value
                              gsm_bahan = row.product_id.x_gsm_bahan


               # Jika belum ada move raw ids
               else:
                    for row_bom in self.bom_id:
                         for bom_line in row_bom.bom_line_ids:
                              categ_product = bom_line.product_id.categ_id.sts_bhn_utama.name
                              if categ_product == 'Bahan Utama':
                                   bahan_utama_mm = bom_line.product_id.x_variant_value
                                   gsm_bahan = bom_line.product_id.x_gsm_bahan

               # Get gram per pcs
               if across_number != 0 or arround_number != 0:
                    panjang_bahan_m = ((qty_to_produce / (across_number * arround_number)) * ref_lebaran_arround) / 1000
                    # pcs_to_m = (((qty_to_produce / (across_number * arround_number)) * (ref_lebaran_arround * 1000))) * (ref_lebaran_across / 1000)
                    pcs_to_m2 = float(panjang_bahan_m) * float(bahan_utama_mm)

                    if gsm_bahan:
                         self.x_gram_stc = pcs_to_m2 * (gsm_bahan + 60)
                    else:
                         self.x_gram_stc = pcs_to_m2 * 140

     # Hitung gram per pcs dari stiker
     @api.one
     def berat_per_pcs(self):
          across_number = self.x_across_number
          arround_number = self.x_arround_number
          across_druk = self.x_across_druk
          arround_druk = self.x_arround_druk
          std_afalan_arround = 0
          std_afalan_across = 0

          if self.x_type_mo == 'stc':
               for product in self.product_id:
                    for line in product.x_layout_product_ids:
                         type = line.x_type
                         if type == 'arround' or type == 'arrounddigital':
                              std_afalan_arround += line.x_std_afalan
                              ref_lebaran_arround =  (arround_number * arround_druk) + std_afalan_arround

                         else:
                              std_afalan_across += line.x_std_afalan
                              ref_lebaran_across = (across_number * across_druk) + std_afalan_across

               # Get lebaran bahan OK (jika sudah ada move raw ids)
               if self.move_raw_ids:
                    for row in self.move_raw_ids:
                         categ_product = row.product_id.categ_id.sts_bhn_utama.name
                         if categ_product == 'Bahan Utama':
                              bahan_utama_mm = row.product_id.x_variant_value
                              gsm_bahan = row.product_id.x_gsm_bahan

               else:
                    for row_bom in self.bom_id:
                         for bom_line in row_bom.bom_line_ids:
                              categ_product = bom_line.product_id.categ_id.sts_bhn_utama.name
                              if categ_product == 'Bahan Utama':
                                   bahan_utama_mm = bom_line.product_id.x_variant_value
                                   gsm_bahan = bom_line.product_id.x_gsm_bahan

               # Get gram per pcs
               if across_number != 0 or arround_number != 0:
                    panjang_bahan_m = (float(1 / float(across_number * arround_number)) * float(ref_lebaran_arround)) / 1000
                    # pcs_to_m = (((qty_to_produce / (across_number * arround_number)) * (ref_lebaran_arround * 1000))) * (ref_lebaran_across / 1000)
                    pcs_to_m2 = float(panjang_bahan_m) * float(bahan_utama_mm)

                    if gsm_bahan:
                         self.x_gram_per_pcs = float(pcs_to_m2) * (gsm_bahan + 60)
                    else:
                         self.x_gram_per_pcs = float(pcs_to_m2) * 140

     @api.one
     def gram_per_lot(self):
          qty_per_pcs = self.x_gram_per_pcs
          hasil = float(qty_per_pcs) * float(self.x_qty_per_lot)
          self.x_berat_per_lot = hasil



class lot_barang(models.Model):
     _name = 'x.lot.barang'
     _inherit = 'mail.thread'
     _description = 'Data Lot Barang'

     x_nomor_ok = fields.Char(string='Nomor OK')
     x_lot_barang = fields.Char(string='Lot Barang')