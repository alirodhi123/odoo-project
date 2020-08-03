# -*- coding: utf-8 -*-
import subprocess

from odoo import models, fields, api, exceptions
import odoo.addons.decimal_precision as dp

class sale_order_line(models.Model):
     _inherit = 'sale.order.line'

     order_id = fields.Many2one('sale.order', string='Order Reference', required=True, ondelete='cascade', index=True,
                                copy=False)
     x_note_so_tree = fields.Text(related='order_id.note', string="Note SO")
     x_confirmation_date_so = fields.Datetime(related='order_id.confirmation_date', string="Confirmation Date SO")
     x_qty_produced_ok = fields.Float(string="Produced", readonly=True)
     x_locked_product_so = fields.Boolean(string="Locked Product", default=True, readonly=True)
     x_status_product = fields.Selection([('false', 'Open'), ('true', 'Locked')], default='true', string="Status Product")
     x_m_qty = fields.Float(string="Quantity (m2)")
     x_reason_dont_need_ok = fields.Text(string="Reason OK")

     # Funsgi tampilkan pop up pesan create OK
     @api.multi
     def pop_message_ok(self):
          product_ok = self.product_id.x_locked_ok
          terms = []

          # Jika prodcut tidak dicentang (Unlock)
          # Jalankan function create OK
          if  product_ok == False:
               for o in self:
                    order_name = o.order_id.id
                    order_name_char = o.order_id.name
                    product_tmpl_id = o.product_tmpl_id

                    bom_obj = self.env['mrp.bom'].search([('product_tmpl_id', '=', product_tmpl_id.id)])
                    if bom_obj:
                         for row in bom_obj:
                              product_text = row.product_tmpl_id.name
                              reference_text = row.code

                              values = {}
                              values['product_text'] = product_text
                              values['reference_text'] = reference_text
                              terms.append((0, 0, values))


               return {
                    'name': 'Create Manufacturing Order',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'pop.message.ok',
                    'target': 'new',
                    'context': {
                         'default_x_sale_order': order_name,
                         'default_x_sale_order_char': order_name_char,
                         'default_x_pop_message_ids': terms,
                         'default_name': "Are you sure want to create Manufacturing Order ?"
                    }
               }

          # Jika product di lock, jalankan function pop up message
          else:
               return {
                    'name': 'Warning',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'pop.message.lock.ok',
                    'target': 'new',
                    'context': {
                         'default_name': "Sorry, Product is Still Locked !",
                         'default_name_second': "Please Request to PDE for Open this Product"
                    }
               }