# -*- coding: utf-8 -*-
import subprocess

from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from datetime import datetime
from odoo.exceptions import UserError


class StockOperationLotInherit(models.Model):
    _inherit = 'stock.pack.operation.lot'

    x_berat_per_lot = fields.Float(string="Berat per Lot (Kg)")

    # Calculate berat per lot
    @api.onchange('qty')
    def calculate_berat_per_lot(self):
        for row in self:
            lot = row.lot_id
            done = row.qty

            stock_production_lot_obj = row.env['stock.production.lot'].search([('id', '=', lot.id)])
            if stock_production_lot_obj:
                for lot in stock_production_lot_obj:
                    berat_per_pcs_lot = float(lot.x_berat_per_pcs_lot)
                    hasil_kg = berat_per_pcs_lot / 1000 # dari gram dijadikan Kg

                row.x_berat_per_lot = done * hasil_kg

