# -*- coding: utf-8 -*-
import subprocess

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp

class sale_order_line(models.Model):
     _inherit = 'sale.order.line'


     # Fungsi parsing data to other view
     @api.multi
     def open_ok_form(self):
          ac = self.env['ir.model.data'].xmlid_to_res_id('mrp.mrp_production_form_view', raise_if_not_found=True)

          for o in self:
               order_id = o.order_id.id
               order_name = o.order_id.name

          result = {
               'name': '2nd class',
               'view_type': 'form',
               'res_model': 'mrp.production',
               'view_id': ac,
               'context': {
                    'default_order': order_id,
                    'default_origin': order_name,
               },
               'type': 'ir.actions.act_window',
               'view_mode': 'form'
          }
          return result






