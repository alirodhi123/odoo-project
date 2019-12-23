# -*- coding: utf-8 -*-
import subprocess
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class mrp_production(models.Model):
     _inherit = 'mrp.production'

     x_buffer_tags = fields.Many2many('buffer.tags', string="Material Location")
     x_tampungan_bu = fields.Text(compute='get_product_bu')
     production_id = fields.Char(string="OK Reference")
     panjang_bahan_bu = fields.Text()
     panjang_bahan_max = fields.Float()
     panjang_bahan_bu_tinta = fields.Char()
     panjang_bahan_laminating_tinta = fields.Char()
     panjang_bahan_pita_tinta = fields.Char()
     panjang_bahan_hot_foil_tinta = fields.Char()
     panjang_bahan_label_tinta = fields.Char()
     date_planned_start = fields.Datetime('Deadline Start', copy=False, default=fields.Datetime.now,index=True, required=True,
                          states={'confirmed': [('readonly', False)]}, oldname="date_planned", track_visibility='onchange')
     date_planned_finished = fields.Datetime('Deadline End', copy=False, index=True, states={'confirmed': [('readonly', False)]},
                                             compute='onchange_date_planned_finished')
     x_is_administrator = fields.Boolean(string="Is Administrator", default=False, compute='get_user_admin')
     x_tgl_produksi = fields.Date(string="Tanggal Turun Produksi")
     x_flag_produksi = fields.Boolean(default=False)

     # WORKORDER
     # Fungsi ambil field finish date yang paling lama
     @api.one
     def onchange_date_planned_finished(self):
         raw_date = 0
         for data in self.workorder_ids:
             if data.date_planned_finished != False:
                 if data.date_planned_finished >= raw_date:
                     raw_date = data.date_planned_finished

         if raw_date != 0:
             self.date_planned_finished = raw_date


     # ORDER KERJA
     # Ambil data dari OK STICKER
     # Untuk Report OK NON STICKER
     @api.onchange('production_id')
     def get_order_kerja(self):
         id = self.production_id
         order_kerja = self.env['mrp.production'].search([('name', '=', id)])
         if order_kerja:
             bu = order_kerja.x_tampungan_bu
             panjang_bahan_max = order_kerja.x_product_uom_qty

             # Pindahkan ke variabel
             self.panjang_bahan_bu = bu
             self.panjang_bahan_max = panjang_bahan_max


     # REPORT
     # Get product BU yg ada di BOM dan tampilkan di report
     # Hanya BU SAJA
     @api.depends('move_raw_ids')
     def get_product_bu(self):

         tampungan = ""
         for row in self.move_raw_ids:
             category_utama = row.product_tmpl_id.categ_id.sts_bhn_utama.name

             if category_utama == "Bahan Utama":
                 if tampungan:
                    tampungan = tampungan + ", " + row.product_id.display_name
                 else:
                    tampungan = row.product_id.display_name

         self.x_tampungan_bu = tampungan


     # MANUFACTURING ORDER
     # Function flagging admin untuk button cancel di OK
     @api.one
     def get_user_admin(self):
         for manufacturing in self:
             state = manufacturing.state
             res_user = manufacturing.env['res.users'].search([('id', '=', manufacturing._uid)])
             # Jika state OK progress atau planned
             if state == "progress" or state == "planned":
                 # Jika login sebagai administrator
                 if res_user.has_group('base.group_system'):
                     manufacturing.update({'x_is_administrator': True})
                 else:
                     manufacturing.update({'x_is_administrator': False})

             # Jika state OK confirmed
             elif state == "confirmed":
                 # Jika login tidak sebagai administrator
                 manufacturing.update({'x_is_administrator': True})
                 pass

     @api.multi
     def production(self):
         for production in self:
            default = datetime.now().strftime('%Y-%m-%d')
            production.update({
                'x_tgl_produksi': default,
                'x_flag_produksi': True
            })









