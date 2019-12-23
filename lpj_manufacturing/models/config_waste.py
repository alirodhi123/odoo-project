# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
import odoo.addons.decimal_precision as dp
import subprocess


class config_waste(models.Model):
     _inherit = 'mrp.production'

     x_trial_produksi = fields.Selection([('trial', 'New Design'), ('not_trial', 'Repeat'), ('barang_trial', 'Trial')],string='Status Produksi:')
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
     x_keb_config = fields.Float(string = 'kebutuhan konfigurasi')
     x_product_uom_qty = fields.Float(string="To consume max", compute='get_max_to_consume')
     product_uom_qty_first = fields.Float(string="To consume min", compute='get_min_to_consume')
     x_duration = fields.Float(string="Duration (hours)", compute='get_duration_hours')
     x_duration_view_custom = fields.Float(string="Duration (minutes)", compute='get_duration_minutes')
     x_duration_view = fields.Float(string="Duration (minutes)", digits=(12, 2))  # syaiful

     @api.multi
     def call_move_raw(self):
          if self.x_trial_produksi == 'trial':
               self.x_value_trial = self.x_std_trial
          else:
               self.x_value_trial = 0

          self.x_keb_config = (( self.x_length_prod * self.x_width_prod * self.product_qty)/(1 - (self.x_waste_config/100)))/self.x_lb_config
          self.x_waste_prod = self.x_std_fixed + ((self.x_std_var / 100) * self.x_keb_config) + self.x_value_trial


     @api.multi
     def confirm_waste(self):
          self.x_last_confirm_waste = self.x_confirm_waste
          for x in self.move_raw_ids:
               category = x.product_tmpl_id.categ_id.name
               category_utama = x.product_tmpl_id.categ_id.sts_bhn_utama.name

               if category_utama == 'Bahan Utama':

                    x.product_uom_qty = x.product_uom_qty + self.x_confirm_waste
                    # To Consume untuk (REPORT)
                    product_uom_qty_temp = x.product_uom_qty
                    self.x_product_uom_qty = product_uom_qty_temp

               if category == 'PL':
                    x.product_uom_qty = x.product_uom_qty + self.x_confirm_waste
               if category == 'DC':
                    x.product_uom_qty = x.product_uom_qty + self.x_confirm_waste

     # Untuk perhitungan confirm waste yg ada di OK Lines
     @api.multi
     def confirm_move_raw(self):
          temp_confirm_waste = self.x_confirm_waste
          # Cek apakah confirm waste sama dengan sebelumnya
          if temp_confirm_waste != self.x_last_confirm_waste:
               for x in self.move_raw_ids:
                    category = x.product_tmpl_id.categ_id.name
                    category_utama = x.product_tmpl_id.categ_id.sts_bhn_utama.name

                    if category_utama == 'Bahan Utama':
                         x.product_uom_qty = x.product_uom_qty + self.x_confirm_waste
                         # To Consume untuk (REPORT)
                         product_uom_qty_temp = x.product_uom_qty
                         self.x_product_uom_qty = product_uom_qty_temp

                    if category == 'PL':
                         x.product_uom_qty = x.product_uom_qty + self.x_confirm_waste
                    if category == 'DC':
                         x.product_uom_qty = x.product_uom_qty + self.x_confirm_waste

          self.x_last_confirm_waste = temp_confirm_waste


     # Untuk simpan BU To consume pada move_raw_ids (REPORT) MINIMAL
     @api.model
     def get_min_to_consume(self):
          for o in self.move_raw_ids:
               category = o.product_tmpl_id.categ_id.name
               category_utama = o.product_tmpl_id.categ_id.sts_bhn_utama.name

               if category_utama == 'Bahan Utama' and category != 'Hot Foil':
                    product_uom_qty_temp = o.product_uom_qty
                    product_uom_qty_first = product_uom_qty_temp - self.x_confirm_waste
                    # Simpan dalam variable baru
                    self.product_uom_qty_first = product_uom_qty_first

               elif category == 'Hot Foil':
                    product_uom_qty_temp = 0
                    min_bahan_hotfoil = o.product_uom_qty

                    if min_bahan_hotfoil != product_uom_qty_temp:
                         # Set bahan hot foil = bahan utama
                         min_bahan_hotfoil = self.x_product_uom_qty
                         # Simpan dalam variable baru
                         self.product_uom_qty_first = min_bahan_hotfoil - self.x_confirm_waste


     # Untuk simpan BU To consume pada move_raw_ids (REPORT) MAXIMAL
     @api.one
     def get_max_to_consume(self):
          for o in self.move_raw_ids:
               category_utama = o.product_tmpl_id.categ_id.sts_bhn_utama.name
               category = o.product_tmpl_id.categ_id.name

               if category_utama == 'Bahan Utama' and category != 'Hot Foil':
                    product_uom_qty_temp = o.product_uom_qty
                    self.x_product_uom_qty = product_uom_qty_temp

               elif category == 'Hot Foil':
                    product_uom_qty_temp = 0
                    max_bahan_hotfoil = o.product_uom_qty
                    if max_bahan_hotfoil != product_uom_qty_temp:
                         # Set bahan hot foil = bahan utama
                         max_bahan_hotfoil = self.x_product_uom_qty
                         # Simpan dalam variable baru
                         self.x_product_uom_qty = max_bahan_hotfoil

     # PERHITUNGAN ESTIMASI TIME
     # Button Method estimasi time
     @api.multi
     def btn_cal_duration(self):
          for production in self:
               hours = 7
               production._get_toconsume()

               # PERHITUNGAN DURATION
               date_format = "%Y-%m-%d %H:%M:%S"
               date_start = production.date_planned_start
               date_finish = production.date_planned_finished

               start_date = datetime.strptime(str(date_start), date_format) + relativedelta(hours=float(hours)) # + GMT 7
               finish_date = datetime.strptime(str(date_finish), date_format) + relativedelta(hours=float(hours)) # + GMT 7

               val_day = ((finish_date - start_date).days * 24) * 60 # Konversi dari Day to Minutes
               val_second = (finish_date - start_date).seconds / 60 # Konversi dari Second to Minutes
               production.x_duration = float(val_day + val_second) / 60 # Konversi dari Minutes to Hours



     # Perhitungan Estimasi Time
     # BY MAS SAIFUL
     @api.multi
     def _get_toconsume(self):
          start_date = self.date_planned_start
          format = "%Y-%m-%d %H:%M:%S"
          start_date_var = datetime.strptime(str(start_date), format)
          start_date_from = datetime.strptime(str(start_date), format)

          for data in self.move_raw_ids:  # edit by syaiful
               internal_category = data.product_tmpl_id.categ_id.sts_bhn_utama.name  # edit by syaiful
               if internal_category == 'Bahan Utama':  # edit by syaiful
                    x_get_consume = data.product_uom_qty  # edit by syaiful
                    break
               else:
                    x_get_consume = 0

          sum_dur_expected = 0
          status_state = 0
          for data in self.workorder_ids:
               ss = data.name
               # get_speed_per_mnt = data.workcenter_id.x_speet_per_mnt
               get_speed_per_mnt = data.operation_id.x_speed_per_mnt

               if get_speed_per_mnt != 0 and x_get_consume != 0:
                    duration_expected = (x_get_consume / get_speed_per_mnt +
                                         data.workcenter_id.time_start +
                                         data.workcenter_id.time_stop)
               else:
                    duration_expected = 0

               if self.state == 'planned':
                    sum_dur_expected += duration_expected
                    date_planned_start = start_date_from
                    date_planned_finished = date_planned_start + relativedelta(hours=float(duration_expected / 60))

                    data.update({
                         'duration_expected': duration_expected,
                         'date_planned_start': date_planned_start,
                         'date_planned_finished': date_planned_finished
                    })
                    start_date_from = datetime.strptime(str(data.date_planned_finished), format)

          if status_state == 1:
               self.x_duration_view = sum_dur_expected
               end_date_val = start_date_var + relativedelta(hours=float(sum_dur_expected / 60))
               self.update({'date_planned_finished': end_date_val})

     # Get durasi hours berdasarkan WO
     @api.model
     def get_duration_hours(self):
          for production in self:
               hours = 7

               # PERHITUNGAN DURATION
               date_format = "%Y-%m-%d %H:%M:%S"
               date_start = production.date_planned_start
               date_finish = production.date_planned_finished

               if date_finish:
                    if date_finish == False:
                         pass

                    else:
                         start_date = datetime.strptime(str(date_start), date_format) + relativedelta(hours=float(hours))  # + GMT 7
                         finish_date = datetime.strptime(str(date_finish), date_format) + relativedelta(hours=float(hours))  # + GMT 7

                         val_day = ((finish_date - start_date).days * 24) * 60  # Konversi dari Day to Minutes
                         val_second = (finish_date - start_date).seconds / 60  # Konversi dari Second to Minutes
                         production.x_duration = float(val_day + val_second) / 60  # Konversi dari Minutes to Hours


     # Konversi durasi dari jam ke menit (sebagai view)
     @api.model
     def get_duration_minutes(self):
          for manufacturing in self:
               duration_hour = manufacturing.x_duration

               # Konversi ke minutes
               duration_minutes = duration_hour * 60
               manufacturing.x_duration_view_custom = duration_minutes


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

class stock_move_variant(models.Model):
     _inherit = 'stock.move'

     x_stockmove_internalref = fields.Char(related='product_id.default_code')
     x_stockmove_variant = fields.Char(readonly=True, compute = '_get_variant_mo')
     x_toconsume_meterpersegi = fields.Float(string = 'To Consume (m2)', readonly=True, compute='_toconsumemeper')
     x_consumed_meterpersegi = fields.Float(string='Consumed (m2)', readonly=True, compute='_consumedmeper')

     @api.one
     def _get_variant_mo(self):
          if self.x_stockmove_internalref:
               self.env.cr.execute("select pav.name from product_attribute_value_product_product_rel ppr "
                                   "left join product_attribute_value pav on ppr.product_attribute_value_id = pav.id "
                                   "left join product_attribute pa on pav.attribute_id = pa.id "
                                   "left join product_product pp on ppr.product_product_id = pp.id "
                                   "left join product_template pt on pp.product_tmpl_id = pt.id "
                                   "where pa.name = 'Lebaran' and pp.default_code = '" + self.x_stockmove_internalref + "'")
               z = self.env.cr.fetchone()
               if z:
                    self.x_stockmove_variant = z[0]
                    self.x_stockmove_variant = (float(self.x_stockmove_variant) / 1000)
                    return self.x_stockmove_variant
               else:
                    return None

     @api.one
     def _toconsumemeper(self):
          self.x_toconsume_meterpersegi = float(self.product_uom_qty) * float(self.x_stockmove_variant)

     @api.one
     def _consumedmeper(self):
          self.x_consumed_meterpersegi = float(self.quantity_done) * float(self.x_stockmove_variant)

