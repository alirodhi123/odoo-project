# -*- coding: utf-8 -*-
import subprocess

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class lot_barang(models.Model):
     _inherit = 'stock.picking'

     x_sj_supplier = fields.Char(string='Nomor Surat Jalan Supplier')
     x_tgl_sj_supp = fields.Datetime(string='Tanggal Surat Jalan Supplier')
     x_tgl_kedatangan_bahan = fields.Datetime(string='Tanggal Terima Bahan')


class stock_line(models.Model):
     _inherit = 'stock.pack.operation'

     keterangan = fields.Text(string="Keterangan")

class sstock_inventory_lot(models.Model):
     _inherit = 'stock.inventory.line'

     x_kode_customer = fields.Char(string = 'Kode Customer')
     @api.multi
     def stock_inventorylot(self):
          return {
               'name': 'Go to website',
               'res_model': 'ir.actions.act_url',
               'type': 'ir.actions.act_url',
               'url': 'http://192.168.1.8:8086/lot/production/lot_adjust?id=4&jumlah=1' + '&name=' + str(
                    self.prod_lot_id.name) + '&bahan=' + '&awal=False' + '&akhir=False' + '&print=1' + '&cus=' + str(self.x_kode_customer) + '&date=' + '&categ= STC' + '&qtyakhir='

               # 'url': 'http://192.168.1.8:8086/lot/production/lot_adjust?id=3&jumlah=' + '&name=' + str(
               #      self.name) + '&bahan=' + '&awal=False' + '&akhir=False' + '&print=' + str(
               #      self.x_jml_print) + '&cus=' + '&date=' + '&categ=' + '&qtyakhir=' + str(
               #      self.x_qty_akhir)
          }




