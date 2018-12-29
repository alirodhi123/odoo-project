# -*- coding: utf-8 -*-
import subprocess

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class config_waste(models.Model):
     _inherit = 'mrp.production'

     x_trial_produksi = fields.Selection([('trial', 'Trial'), ('not_trial', 'Bukan Trial')],string='Status Produksi:')
     x_mesin = fields.Many2one('mrp.workcenter', string='Mesin: ')
     x_std_fixed = fields.Float(related = 'x_mesin.x_std_waste.x_fixed_m')
     x_std_var = fields.Float(related='x_mesin.x_std_waste.x_variable')
     x_std_trial = fields.Float(related='x_mesin.x_std_waste.x_trial')
     x_config_factor = fields.Many2one('x.config.factor.waste', required = True, string = 'Configurasi')
     x_lb_config = fields.Float(related = 'x_config_factor.x_lebar_configurasi')
     x_pj_config = fields.Float(related = 'x_config_factor.x_panjang_configurasi')
     x_waste_config = fields.Float(related='x_config_factor.x_waste_configuration')
     x_value_trial = fields.Float(string = 'Value_trial')

     x_length_prod = fields.Float(related = 'product_id.x_length_m')
     x_width_prod = fields.Float(related = 'product_id.x_width_m')
     x_bahan_utama = fields.Many2one(string='Bahan Utama', related='move_raw_ids.product_id')
     x_uom_qty = fields.Float(string = 'quantity bahan', related = 'move_raw_ids.product_uom_qty')
     x_waste_prod = fields.Float(string = 'Waste Produksi')
     x_confirm_waste = fields.Float(string = 'Confirm Waste', default = 0)
     x_last_confirm_waste = fields.Float(string = 'Confirm Last Waste', default = 0, help = 'fields ini digunakan untuk save last confirm waste')
     x_coba = fields.Char(string = 'tampungann saja ')
     x_keb_config = fields.Float(string = 'kebutuhan konfigurasi')
     x_product_uom_qty = fields.Float(string="To consume")

     @api.multi
     def call_move_raw(self):
          if self.x_trial_produksi == 'trial':
               self.x_value_trial = self.x_std_trial
          else:
               self.x_value_trial = 0
          self.x_keb_config = (( self.x_length_prod * self.x_width_prod * self.product_qty)/(1 - (self.x_waste_config/100)))/self.x_lb_config
          self.x_waste_prod = self.x_std_fixed + ((self.x_std_var / 100) * self.x_keb_config) + self.x_value_trial

     @api.onchange('x_confirm_waste')
     def confirm_waste(self):
          self.x_last_confirm_waste = self.x_confirm_waste
          for x in self.move_raw_ids:
               self.x_coba = x.product_tmpl_id.categ_id.name
               if x.product_tmpl_id.categ_id.name == 'BU':
                    x.product_uom_qty = x.product_uom_qty + self.x_confirm_waste
                    # To Consume untuk report
                    product_uom_qty_temp = x.product_uom_qty
                    self.x_product_uom_qty = product_uom_qty_temp

               if x.product_tmpl_id.categ_id.name == 'PL':
                    x.product_uom_qty = x.product_uom_qty + self.x_confirm_waste
               if x.product_tmpl_id.categ_id.name == 'DC':
                    x.product_uom_qty = x.product_uom_qty + self.x_confirm_waste


               # if x.product_id.categ_id == '8':
               #      x.move_raw_ids.product_uom_qty = 200
                    # x.move_raw_ids.product_uom_qty = x.move_raw_ids.product_uom_qty + self.x_confirm_waste
                    # self.x_uom_qty = self.x_uom_qty + self.x_confirm_waste


          # Get qty product to consume for report lenght OK
          @api.onchange('x_confirm_waste')
          def get_to_consume(self):
               for o in self.move_raw_ids:
                    categ = o.product_tmpl_id.categ_id.name
                    if categ == "BU":
                         product_uom_qty_temp = o.product_uom_qty

                    self.x_product_uom_qty = product_uom_qty_temp


class master_config_waste(models.Model):
     _name = 'x.standart.waste.produksi'

     x_mesin = fields.Many2one('mrp.workcenter', string = 'Mesin: ')
     x_fixed_m = fields.Float(string = 'Fixed [m]')
     x_variable = fields.Float(string = 'Variable [%/m]', help = 'Berdasarkan Total Weblength Kebutuhan Configuration')
     x_trial = fields.Float(string = 'Trial [m]')

class config_factor_waste(models.Model):
     _name = 'x.config.factor.waste'

     name = fields.Char (default = '[Used] Factor Waste Configuration', readonly = True, help = '[used] config yg digunakan, pastikan tidak ada double [used]')
     x_waste_configuration = fields.Float (string = 'Waste Configuration (%)')
     x_lebar_configurasi = fields.Float(string = 'Lebar Configurasi [m]')
     x_panjang_configurasi = fields.Float(string='Panjang Configurasi [m]')
     x_toleransi_produksi = fields.Float(string = 'Toleransi Produksi [%]')

class master_config_waste(models.Model):
     _inherit = 'mrp.workcenter'

     x_std_waste = fields.One2many('x.standart.waste.produksi','x_mesin', string = 'standart waste')

# class move_raw(models.Model):
#      _inherit = 'stock.move'

     # @api.one
     # def cal_waste(self):
     #      self.x_total_waste = 10.5

          # if self.x_trial_produksi == 'trial':
          #      self.x_value_trial = self.x_std_trial
          # else:
          #      self.x_value_trial = 0
          # self.x_total_waste = self.x_std_fixed + ((self.x_std_var / 100) * self.product_uom_qty) + self.x_value_trial




