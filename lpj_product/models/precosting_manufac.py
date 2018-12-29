# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp

class precost_custom(models.Model):
     _inherit = 'product.template'

     # PLATE SIZE CAL
     x_prepres_saffac = fields.Float(string='Prepress Safety Factor')
     x_n_cross = fields.Integer(string='n_cross')
     x_gap = fields.Float(string='n_cross')
     x_side = fields.Float(string='side')
     x_die_width = fields.Float(string='die width')
     x_printing_length = fields.Float(string='Printing Length')
     x_NoU = fields.Float(string='Number of Up')
     x_single_plate_area = fields.Float(string='Single Plate Area')
     x_total_plate_area = fields.Float(string='Total Plate Area')
     x_plate_width = fields.Float(string='Plate Width')
     x_plate_Length = fields.Float(string='Plate Length')

     #LABEL MATERIAL CAL
     x_owt = fields.Float(string='Operator Waste Target', readonly=True)
     x_material_width_tolerance = fields.Float(string='Material Width Tolerance', readonly=True)
     x_paper_density = fields.Float(string='Paper Density', readonly=True)
     x_finished_product_areapcs = fields.Float(string='Finished Product Area per Pcs', readonly=True)
     x_product_area = fields.Float(string='Product Area', readonly=True)
     x_plate_area = fields.Float(string='Plate Area', readonly=True)
     x_WC_Plate_Width = fields.Float(string='Worst-Case Plate Width', readonly=True)
     x_adjusted_plate_area = fields.Float(string='Adjusted Plate Area', readonly=True)
     x_config_waste_percent = fields.Float(string='Config Waste Percentage', readonly=True)
     x_eff_config_waste_percent = fields.Float(string='Effective Config Waste Percentage', readonly=True)
     x_config_wastepcs = fields.Float(string='Config Waste per Pcs', readonly=True)
     x_tot_config_waste = fields.Float(string='Total Config Waste', readonly=True)
     x_owtp = fields.Float(string='Operator Waste Target per Pcs', readonly=True)
     x_tot_area = fields.Float(string='Total Manufacturing Area', readonly=True)


     #INK USAGE CAL
     x_ink_usage_safac = fields.Float(string='Ink Usage Safety Factor', readonly=True)
     x_ink_usage_density = fields.Float(string='Ink Usage Density', readonly=True)
     x_fixed_ink_sw = fields.Float(string='Fixed Ink Setup Waste', readonly=True)
     x_spec_color = fields.Float(string='Special Color Usage', readonly=True)
     x_varnish_color = fields.Float(string='Varnish Color Usage', readonly=True)

     #EXTRA MISC CAL -- tidak bisa ditampilkan karena semua berhubungan dengan cost dan terhitung bersama QTY
     #DIECUT CAL
     x_speed = fields.Float(string='Speed')
     x_setup_time = fields.Float(string='Setup Time')


