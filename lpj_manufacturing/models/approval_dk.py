# -*- coding: utf-8 -*-
import subprocess

from odoo import models, fields, api, exceptions
import odoo.addons.decimal_precision as dp
from datetime import datetime, time
from dateutil.relativedelta import relativedelta

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
     # x_tgl_kirim_pertama = fields.Datetime(string="Tanggal Kirim Pertama", related="name.x_req_dk_pertama", track_visibility='onchange')
     x_tgl_keputusan = fields.Datetime(string="Tanggal pemberian keputusan")
     x_flag_reqdk = fields.Boolean(default = False,related="name.x_flag_reqdk")
     x_flag_appdk = fields.Boolean(default = False,related="name.x_flag_appdk")
     x_mesin = fields.Many2one('mrp.workcenter', 'Prime Machine', related = "name.x_mrpwordkcenter_id", readonly = True)
     x_manufacturing_type = fields.Selection([('laprint', 'Laprint'), ('digital', 'Digital')],
                                             default='laprint', string='Manufacturing Type', related='name.x_manufacturing_type',
                                             track_visibility='onchange', required=True)
     x_planning_type = fields.Selection([('forward', 'Forward Planning'), ('backward', 'Backward Planning')],
                                        default='forward', string='Planning Type', related='name.x_planning_type',
                                        track_visibility='onchange', required=True)
     x_quantity_m2 = fields.Float(string="Qty m2", compute='compute_qty_m2')

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

     @api.one
     def compute_qty_m2(self):
          for row in self:
               qty = row.x_qty
               sales_quotation = row.name

               for o in sales_quotation:
                    product = o.x_product

                    if product:
                         lenght_m = product.x_length / 1000
                         width_m = product.x_width / 1000

                         row.x_quantity_m2 = (lenght_m * width_m * qty) / 0.75

                    else:
                        lenght_m = o.x_length / 1000
                        width_m = o.x_width / 1000

                        row.x_quantity_m2 = (lenght_m * width_m * qty) / 0.75


class config_default_duedate(models.Model):
    _name = 'x.config.default.duedate'

    name = fields.Char(string='Kategori')
    x_day = fields.Integer(string='Nilai')

    @api.model
    def duedate_kirim(self):
        a = int(datetime.now().strftime("%w"))
        if a < 6:
            self.env.cr.execute(
                "select id, x_tgl_request, x_status_dk, x_repeat_order from x_sales_quotation where x_tgl_request is not null")
            sql = self.env.cr.fetchall()
            for o in sql:
                id = o[0]
                repeat = o[3]
                status = 'New'
                if repeat == True:
                     status = 'Repeat'

                self.env.cr.execute(
                     "select x_day from x_config_default_duedate where name = '"+ str(status) +"'")
                sql2 = self.env.cr.fetchone()
                self.env.cr.execute(
                    "select x_day from x_config_default_duedate where name = 'Reset'")
                sql3 = self.env.cr.fetchone()
                self.env.cr.execute(
                    "select x_day from x_config_default_duedate where name = 'Workday'")
                sql4 = self.env.cr.fetchone()
                if o[1]:
                    if o[2] == 'approve' or o[2] == 'reject' or o[2] == 'draft':
                        a = datetime.now()


                    else:
                        date_format = "%Y-%m-%d %H:%M:%S"
                        tgl_req = o[1]
                        day=sql2[0]
                        hour=sql3[0]
                        workday=sql4[0]
                        batas_tgl = datetime.strptime(str(tgl_req), date_format) + relativedelta(hours=float(hour))
                        tgl_default = datetime.strptime(str(tgl_req), date_format)
                        while day > 0:
                            tgl_default += relativedelta(days=1)
                            weekday = tgl_default.weekday()
                            if weekday >= workday:  # sunday = 6
                                continue
                            day -= 1

                        tgl_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        if batas_tgl < datetime.now():
                            # app_dk = self.env['x.approval.dk'].browse([(id)])
                            # if app_dk:
                            #     self.env['x.approval.dk'].update({
                            #         'x_tgl_keputusan': datetime.now()
                            #     })

                            sq = self.env['x.sales.quotation'].search([('id', '=', id)])
                            if sq:
                                sq.update({
                                    'x_flag_appdk': True,
                                    'x_status_dk': 'approve',
                                    'x_req_dk': tgl_default,
                                })

                            self.env.cr.execute(
                                "UPDATE x_approval_dk SET write_uid = '1', x_tgl_keputusan='" +
                                str(tgl_sekarang) + "'  WHERE name = '" + str(id) + "'")










                            # self.env.cr.execute(
                            #     "UPDATE x_sales_quotation SET x_flag_appdk = 't', x_status_dk= 'approve', x_req_dk='" +
                            #     str(tgl_default) + "'  WHERE id = '" + str(id) + "'")


    @api.model
    def reset_duedate(self):
        a = int(datetime.now().strftime("%w"))
        if a < 6:
            self.env.cr.execute(
                "select quot.id, quot.x_tgl_request, quot.x_status_dk, sol.id so_line, app.x_tgl_keputusan "
                "from x_sales_quotation quot "
                "join x_approval_dk app on app.name = quot.id "
                "left join sale_order_line sol on sol.x_customer_requirement = quot.name "
                "where sol.id is null and x_status_dk = 'approve'")
            sql = self.env.cr.fetchall()
            for o in sql:
                id = o[0]
                self.env.cr.execute(
                    "select x_day from x_config_default_duedate where name = 'Reset'")
                sql3 = self.env.cr.fetchone()
                if o[4]:
                    date_format = "%Y-%m-%d %H:%M:%S"
                    tgl_kep = o[4]
                    hour = sql3[0]
                    batas_tgl = datetime.strptime(str(tgl_kep), date_format) + relativedelta(hours=float(hour))
                    tgl_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if batas_tgl < datetime.now():
                        # app_dk = self.env['x.approval.dk'].browse([(id)])
                        # if app_dk:
                        #     self.env['x.approval.dk'].update({
                        #         'x_tgl_keputusan': datetime.now()
                        #     })

                        sq = self.env['x.sales.quotation'].search([('id', '=', id)])
                        if sq:
                            sq.update({
                                'x_flag_appdk': False,
                                'x_flag_reqdk': False,
                                'x_status_dk': 'draft',
                            })

