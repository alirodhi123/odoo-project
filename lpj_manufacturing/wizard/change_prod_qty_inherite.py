# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_is_zero
import math

class ChangeProductionQtyInherit(models.TransientModel):
    _inherit = 'change.production.qty'



    # CUSTOM FUNCTION UPDATE QTY PRODUCED
    @api.multi
    def update_qty_produced(self):
        quantity_to_produce = self.product_qty
        mo_id = self.mo_id

        if mo_id:
            for o in mo_id:
                order = o.order
                type_mo = o.x_type_mo
                x_qtytoproduce_temp = o.x_qtytoproduce_temp

                if type_mo == 'stc' and order:
                    sale_order_obj = self.env['sale.order'].search([('id', '=', order.id)])
                    product_ok = o.product_id

                    if sale_order_obj:
                        for order_line in sale_order_obj.order_line:
                            product_so = order_line.product_id
                            ordered_qty = order_line.product_uom_qty

                            if product_so == product_ok:
                                # Jika masih dalam OK yang sama
                                if mo_id.id == o.x_temp_mo and quantity_to_produce <= x_qtytoproduce_temp:
                                    temp_produced_ok = quantity_to_produce
                                    qty_produced_so = order_line.x_qty_produced_ok

                                    # Perhitungan
                                    sementara = x_qtytoproduce_temp - temp_produced_ok
                                    hasil = qty_produced_so - sementara

                                    order_line.update({'x_qty_produced_ok': hasil})

                                    o.x_temp_mo = mo_id
                                    o.x_qtytoproduce_temp = temp_produced_ok

                                    if order_line.x_qty_produced_ok >= ordered_qty:
                                        order_line.update({'x_flag_mo': True})
                                    else:
                                        order_line.update({'x_flag_mo': False})


                                elif mo_id.id == o.x_temp_mo and quantity_to_produce > x_qtytoproduce_temp:
                                    temp_produced_ok = quantity_to_produce
                                    qty_produced_so = order_line.x_qty_produced_ok

                                    # Perhitungan
                                    sementara = temp_produced_ok - x_qtytoproduce_temp
                                    hasil = qty_produced_so + sementara

                                    order_line.update({'x_qty_produced_ok': hasil})

                                    o.x_temp_mo = mo_id
                                    o.x_qtytoproduce_temp = temp_produced_ok

                                    if order_line.x_qty_produced_ok >= ordered_qty:
                                        order_line.update({'x_flag_mo': True})
                                    else:
                                        order_line.update({'x_flag_mo': False})

                                else:
                                    temp_produced_ok = quantity_to_produce + order_line.x_qty_produced_ok
                                    order_line.update({'x_qty_produced_ok': temp_produced_ok})
                                    o.x_temp_mo = mo_id.id
                                    o.x_qtytoproduce_temp = quantity_to_produce

                                    # Update flagging x_flag_mo jika produced qty >= ordered qty
                                    if order_line.x_qty_produced_ok >= ordered_qty:
                                        order_line.update({'x_flag_mo': True})
                                    else:
                                        order_line.update({'x_flag_mo': False})

    # INHERIT FUNCTION UPDATE QTY
    @api.multi
    def change_prod_qty(self):
        self.update_qty_produced()

        res = super(ChangeProductionQtyInherit, self).change_prod_qty()
        return res