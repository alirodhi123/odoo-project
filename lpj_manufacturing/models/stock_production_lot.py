from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Production_lots(models.Model):
    _inherit = 'stock.move.lots'

    # LOT REFERENCE
    x_lot_reference = fields.Char(string="Lot Reference", readonly=True)
    x_product_id = fields.Char(string="Product")

    # CEK QTY PRODUCT WIP
    # Cek qty product untuk per line WO
    # @api.onchange('lot_id', 'quantity_done')
    # def check_qty_wip(self):
    #     for row in self:
    #         lot_wip = 0
    #         qty_wip = 0
    #         stock_location = 0
    #         lot_id = 0
    #         product_id = 0
    #         qty_done = 0
    #
    #         product_id = row.product_id
    #         lot_id = row.lot_id
    #         qty_done = row.quantity_done
    #
    #         stock_quant_obj = row.env['stock.quant'].search([('product_id', '=', product_id.id)])
    #         if stock_quant_obj:
    #             for stock in stock_quant_obj:
    #                 wip_location = stock.location_id.id
    #
    #                 # Jika lokasi stock di WIP
    #                 if wip_location == 22:
    #                     lot_wip = stock.lot_id
    #                     qty_wip += stock.qty
    #
    #             # Jika qty done > qty wip dan lot wo == lot wip maka error
    #             if qty_done > qty_wip and lot_id == lot_wip:
    #                 raise UserError(_(
    #                     'Quantity is not enough, please check the quantity on hand of (' + product_id.barcode + ') in WIP !'))


class Lot_Work_Order(models.Model):
    _name = 'x.move.lots'

    workorder_id = fields.Many2one('mrp.workorder')
    x_lot = fields.Char(string="Lot")
    x_product_id = fields.Many2one('product.product', string="Product")
    x_to_consume = fields.Char(string="To Consume")



