# -*- coding: utf-8 -*-
import subprocess

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp

class sq(models.Model):
    _inherit = 'x.cusrequirement'
    x_so_line= fields.One2many('sale.order.line', 'x_customer_requirement', string='hub SQ ke SO line')


class minmax_mo(models.Model):
     _inherit = 'mrp.production'

     x_type_mo = fields.Selection([('stc', 'Sticker'), ('ink', 'Tinta Campuran'), ('plate', 'Plate'),('diecut', 'Diecut')], string='Type MO')
     x_quantity_max = fields.Float(string = 'Quantity Maksimal')

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

     x_toleransi = fields.Float(string = 'Toleransi', related ='orderline.x_toleransi')

     jml_lot = fields.Char(string='Jumlah Lot')
     x_kode_awal = fields.Char(string='Kode Awal')
     x_kode_akhir = fields.Char(string='Kode Akhir')
     jml_print = fields.Char(string='Jumlah Print', default=2)
     x_type_print = fields.Selection([('all', 'All'), ('specific', 'Specific')], string='Type Print out', default = 'all')
     x_keterangan = fields.Text(string="Keterangan")
     x_qty_so = fields.Float(string="Quantity SO")
     x_qty_so_toleransi = fields.Float(string="Quantity SO Toleransi", compute='get_qty_so_toleransi')
     x_width = fields.Float(string="Width")

     @api.onchange('orderline', 'x_qty_so', 'product_qty', 'x_toleransi')
     def set_value(self):
          product_qty = self.product_qty
          qty_so = self.x_qty_so
          toleransi = self.x_toleransi

          if self.x_type_mo == 'stc':
               self.product_id = self.x_kode_product

          self.x_quantity_max = ((self.x_toleransi / 100) * self.product_qty) + self.product_qty

          self.x_qty_so = product_qty


     @api.depends('x_toleransi', 'x_qty_so')
     def get_qty_so_toleransi(self):
          qty_so = self.x_qty_so
          toleransi = self.x_toleransi

          val_toleransi = ((toleransi / 100) * qty_so) + qty_so
          self.x_qty_so_toleransi = val_toleransi

     @api.model
     def create(self, vals):
          vals['x_flag'] = True
          result = super(minmax_mo, self).create(vals)
          return result

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

     # Get one2many x_layout_product_ids
     @api.onchange('product_id')
     def get_value(self):

          id = self.product_id.id
          accros = self.env['product.product'].search([('id', '=', id)])
          for o in accros.x_layout_product_ids:
               type = o.x_type
               variable = o.x_jumlah

               if type == "across":
                    self.x_width = variable


class lot_barang(models.Model):
     _name = 'x.lot.barang'
     _inherit = 'mail.thread'
     _description = 'Data Lot Barang'

     x_nomor_ok = fields.Char(string='Nomor OK')
     x_lot_barang = fields.Char(string='Lot Barang')