# -*- coding: utf-8 -*-
import subprocess

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp

class sq(models.Model):
    _inherit = 'x.cusrequirement'
    x_so_line= fields.One2many('sale.order.line', 'x_customer_requirement', string='hub SQ ke SO line')


class minmax_mo(models.Model):
     _inherit = 'mrp.production'

     x_type_mo = fields.Selection([('stc', 'Sticker'), ('ink', 'Tinta Campuran'), ('plate', 'Plate'),('diecut', 'Diecut')], string='Type MO', required=True)
     order = fields.Many2one('sale.order', string = 'Kode SO')
     orderline = fields.Many2one('sale.order.line', string = 'Barang SO')
     x_flag = fields.Boolean(related = 'orderline.x_flag_mo')
     x_due_kirim = fields.Datetime(related = 'orderline.x_duedate_kirim', readonly=True)

     # x_sale_order = fields.Many2one('sale.order', string="Sale Order", help="Select Sale Order")
     # x_order_id = fields.Char(related = 'x_sale_order.order_id')
     # x_sale_order_line = fields.Many2one('sale.order.line')
     x_kode_product = fields.Many2one('product.product',related='orderline.product_id')
     # product_id = fields.Many2one('product.product', readonly = True, store=True, string="Order Reference Product", help="Select product", related='orderline.product_id')
     # x_product_temp = fields.Many2one('product.product', readonly=True, store=True, string="Product Related",
     #                                   help="Select product", related='x_sale_order_line.product_id')
     # x_product_temp = fields.Many2one('product.product', readonly=True, store=True, string="Product Related",
     #                                  help="Select product", related='cusrequire.x_product')
     customer = fields.Many2one('res.partner', string='Customer', related = 'order.partner_id')
     customer_code = fields.Char(related = 'customer.x_kode_customer')
     categ_id = fields.Many2one(readonly = True, related = 'product_id.product_tmpl_id.categ_id')


     # order_line = fields.One2many('sale.order.line', 'x_sol', string='Order Lines', related = 'cusrequire.x_so_line')
     # x_toleransi_pengiriman = fields.Integer(related = 'order_line.x_toleransi', readonly = True, string = 'Toleransi')

     x_toleransi = fields.Float(string = 'Toleransi SO', related ='orderline.x_toleransi')

     jml_lot = fields.Char(string='Jumlah Lot')
     x_kode_awal = fields.Char(string='Kode Awal')
     x_kode_akhir = fields.Char(string='Kode Akhir')
     jml_print = fields.Char(string='Jumlah Print', default=2)
     x_type_print = fields.Selection([('all', 'All'), ('specific', 'Specific')], string='Type Print out', default = 'all')
     x_keterangan = fields.Text(string="Keterangan")
     x_width = fields.Float(string="Width", compute='get_value')
     quantity_so = fields.Float(string="Quantity SO", compute='get_value_qty_so')

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


     @api.model
     def create(self, vals):
          vals['x_flag'] = True
          result = super(minmax_mo, self).create(vals)
          return result

     # Onchange product
     @api.onchange('x_type_mo')
     def set_value(self):
          if self.x_type_mo == 'stc':
               # Jika orderline kosong
               if self.orderline.id == False:
                    self.product_id = self.product_id
               else:
                    self.product_id = self.x_kode_product

     # @api.multi
     # def write(self, vals):
     #      vals['x_flag'] = True
     #      return super(minmax_mo, self).write(vals)

     @api.multi
     def action_next(self):
          return {
               'name': 'Go to website',
               'res_model': 'ir.actions.act_url',
               'type': 'ir.actions.act_url',
               'url': 'http://192.168.1.8:8086/lot/production/lot_barang?id=1&jumlah=' + self.jml_lot + '&awal=' + str(self.x_kode_awal) + '&akhir=' + str(self.x_kode_akhir) + '&name=' + self.name + '&print=' + self.jml_print + '&categ=' + str(self.categ_id.name)+ '&cus=' + str(self.customer_code)+'&date=' + self.date_planned_start+'&qtyakhir=False'
               # 'url': 'http://192.168.2.40:8086/world.php?jumlah='+ self.jml_lot
               # 'url': 'http://192.168.1.8:8081/Lot?id=1&jumlah=' + self.jml_lot +'&name='+ self.name
          }

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

               if type == "across":
                    self.x_width = variable

               # get value arround (REPORT)
               elif type == "arround":
                    self.x_jarak_druk = jarak_druk  # Satuan mm


     # Get one2many order_line qty SO (REPORT)
     @api.depends('product_id', 'x_toleransi')
     def get_value_qty_so(self):

          toleransi_so = self.x_toleransi
          id = self.order.id
          qty_so = self.env['sale.order'].search([('id', '=', id)])
          for o in qty_so.order_line:
               if self.product_id == o.product_id:
                    # Get qty SO REAL
                    qty = o.product_uom_qty
                    # Menghitung TOLERANSI + QTY SO REAL
                    valToleransi = ((toleransi_so / 100) * qty) # (5/100) : 20000 = 1000
                    valQtyFix = valToleransi + qty # Hasil toleransi + qty SO REAL (1000 + 20000)
                    # Put in new variable
                    self.quantity_so = valQtyFix

     # Convert pcs to meter untuk REPORT OK
     @api.depends('x_jarak_druk', 'x_pcs_units')
     def convert_pcs_to_meter(self):
          hasil = self.x_pcs_units * self.x_jarak_druk #Masih dalam mm
          self.pcs_to_meter = hasil / 1000 # Convert hasil (mm) ke meter


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
               if type == "across":
                    self.x_isi_druk = isi_druk # Get isi druk dari accross
               else:
                    self.x_jarak_druk_product = jarak_druk # Get jarak druk dari arround


     # PERHITUNGAN QTY MAX
     # Qty max berdasarkan stock yang ada di gudang gudang
     # REPORT
     @api.depends('quantity_so', 'x_toleransi', 'product_qty', 'x_product_uom_qty', 'x_isi_druk', 'x_jarak_druk_product')
     def compute_max_qty(self):
          qty_so = self.quantity_so
          toleransi_so = self.x_toleransi
          qty_to_produce = self.product_qty
          isi_druk = self.x_isi_druk
          jarak_druk = self.x_jarak_druk_product / 10 #konversi mm ke cm
          panjang_bahan_max = self.x_product_uom_qty

          if jarak_druk != 0:
               qty_max_temp = (panjang_bahan_max * isi_druk) / jarak_druk
               qty_max = qty_max_temp * 100
               self.x_quantity_max = qty_max


     # REPORT JUMLAH DRUK
     # Get jumlah druk MAX dan jumlah druk MIN dari product
     # Model Product.product
     @api.one
     def get_jumlah_druk(self):
          id = self.product_id.id
          product_product = self.env['product.product'].search([('id', '=', id)])
          if product_product:
               for row in product_product.x_layout_plong_ids:
                    if row.x_plong_type == 'across':
                         across_number = row.x_plong_number
                         self.x_across_number = across_number
                    else:
                         arround_number = row.x_plong_number
                         self.x_arround_number = arround_number


     # PERHITUNGAN JUMLAH DRUK MAX DAN MINIMAL
     # Ambil dari fungsi get_jumlah_druk
     @api.depends('product_qty', 'x_quantity_max', 'x_across_number', 'x_arround_number')
     def calculate_jumlah_druk(self):
          qty_to_produce = self.product_qty
          qty_max = self.x_quantity_max
          var_across_number = self.x_across_number
          var_arround_number = self.x_arround_number

          if var_across_number != 0 and var_arround_number != 0:
               druk_min = qty_to_produce / (var_across_number * var_arround_number)
               druk_max = qty_max / (var_across_number * var_arround_number)
               self.jumlah_druk_min = druk_min
               self.jumlah_druk_max = druk_max


class lot_barang(models.Model):
     _name = 'x.lot.barang'
     _inherit = 'mail.thread'
     _description = 'Data Lot Barang'

     x_nomor_ok = fields.Char(string='Nomor OK')
     x_lot_barang = fields.Char(string='Lot Barang')