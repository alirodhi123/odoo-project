# -*- coding: utf-8 -*-
import subprocess

from odoo import models, fields, api, exceptions
import odoo.addons.decimal_precision as dp
from datetime import datetime, time

class approval_duedate_kirim(models.Model):
     _name = 'x.approval.dk'
     _inherit = 'mail.thread'

     name = fields.Many2one('x.sales.quotation', readonly = True)
     x_sales = fields.Many2one('res.partner', related = "name.x_sales_id", readonly = True)
     x_material_type_id = fields.Many2one('product.template', 'Material Type', related = "name.x_material_type_id",readonly = True)
     # x_acc_cust = fields.Datetime(string="Tanggal ACC Design Cust",readonly = True,related = "name.x_tgl_acc_drawing",)
     x_customer = fields.Many2one('res.partner', related="name.x_customer_id", readonly = True)
     x_item = fields.Char(String = "Item Name",related="name.item_description", readonly = True)
     x_qty = fields.Integer(string = "Quantity", related = "name.x_qty", readonly = True)
     x_tgl_kirim = fields.Datetime(string="Tanggal Kirim", related="name.x_req_dk", track_visibility='onchange')
     x_tgl_keputusan = fields.Datetime(string="Tanggal pemberian keputusan")
     x_flag_reqdk = fields.Boolean(default = False,related="name.x_flag_reqdk")
     x_flag_appdk = fields.Boolean(default = False,related="name.x_flag_appdk")
     x_mesin = fields.Many2one('mrp.workcenter', 'Prime Machine', related = "name.x_mrpwordkcenter_id", readonly = True)

     @api.multi
     def act_approve_dk(self):
          self.x_flag_appdk = True
          self.name.x_flag_appdk = True
          self.x_tgl_keputusan =  datetime.now()
          self.name.x_status_dk = 'approve'

     @api.multi
     def act_reject_dk(self):
          self.x_flag_reqdk = False
          self.name.x_flag_reqdk = False
          self.x_tgl_keputusan = datetime.now()
          self.name.x_status_dk = 'reject'