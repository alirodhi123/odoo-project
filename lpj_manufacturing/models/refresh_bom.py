from odoo import models, fields, api
from odoo.exceptions import UserError


class refresh_bom(models.Model):
    _inherit = 'mrp.production'

    @api.multi
    def compare_bom(self):
        for production in self:
            production.delete_bom() # Delete terlebih dahulu bom line yang ada di OK
            production.delete_stock_move() # Delete terlebih dahulu barang yang ada di stock move (Tracebility)
            factor = production.product_uom_id._compute_quantity(production.product_qty, production.bom_id.product_uom_id) / production.bom_id.product_qty
            boms, lines = production.bom_id.explode(production.product_id, factor, picking_type=production.bom_id.picking_type_id)
            production._generate_raw_moves_custom(lines)
            # Check for all draftconfirm_waste moves whether they are mto or not
            production._adjust_procure_method()
            production.move_raw_ids.action_confirm()
            production.confirm_waste() # Perhitungan confirm waste
            for row in production.move_raw_ids:
                if row.quantity_available != 0 or row.quantity_available == 0:
                    production.action_assign()

            # Menampilkan pop up message
            if production:
                return production.my_custom_button_function_for_another_wizard()

        return True

    def _generate_raw_moves_custom(self, exploded_lines):
        self.ensure_one()
        moves = self.env['stock.move']
        for bom_line, line_data in exploded_lines:
            moves += self._generate_raw_move_custom(bom_line, line_data)
        return moves

    def _generate_raw_move_custom(self, bom_line, line_data):
        quantity = line_data['qty']
        # alt_op needed for the case when you explode phantom bom and all the lines will be consumed in the operation given by the parent bom line
        alt_op = line_data['parent_line'] and line_data['parent_line'].operation_id.id or False
        if bom_line.child_bom_id and bom_line.child_bom_id.type == 'phantom':
            return self.env['stock.move']
        if bom_line.product_id.type not in ['product', 'consu']:
            return self.env['stock.move']
        if self.routing_id:
            routing = self.routing_id
        else:
            routing = self.bom_id.routing_id
        if routing and routing.location_id:
            source_location = routing.location_id
        else:
            source_location = self.location_src_id
        original_quantity = (self.product_qty - self.qty_produced) or 1.0
        data = {
            'sequence': bom_line.sequence,
            'name': self.name,
            'date': self.date_planned_start,
            'date_expected': self.date_planned_start,
            'bom_line_id': bom_line.id,
            'product_id': bom_line.product_id.id,
            'product_uom_qty': quantity,
            'product_uom': bom_line.product_uom_id.id,
            'location_id': source_location.id,
            'location_dest_id': self.product_id.property_stock_production.id,
            'raw_material_production_id': self.id,
            'company_id': self.company_id.id,
            'operation_id': bom_line.operation_id.id or alt_op,
            'price_unit': bom_line.product_id.standard_price,
            'procure_method': 'make_to_stock',
            'origin': self.name,
            'warehouse_id': source_location.get_warehouse().id,
            'group_id': self.procurement_group_id.id,
            'propagate': self.propagate,
            'unit_factor': quantity / original_quantity,
        }
        return self.env['stock.move'].create(data)

    # Fungsi delete record pada stock move (Tracebility)
    @api.multi
    def delete_stock_move(self):
        stock = self.env['stock.move'].search([('origin', '=', self.name),('production_id', '=', False)])
        if stock:
            # Sebelum hapus ubah state menjadi draft
            stock.write({'state': 'draft'})
            return stock.unlink()

    # Fungsi untuk delete semua record move_raw_ids
    @api.multi
    def delete_bom(self):
        bom_ids_line = []
        bom_id = self.bom_id
        quantity_ok = self.product_qty
        bom = self.env['mrp.bom'].search([('id', '=', bom_id.id)])
        if bom:
            for row in bom:
                # Looping bom line ids
                for line in row.bom_line_ids:
                    bom_ids_line.append(([5]))

                return self.update({'move_raw_ids': bom_ids_line})


    # Funsgi tampilkan pop up pesan
    @api.multi
    def my_custom_button_function_for_another_wizard(self):
        return {
            'name': 'Success',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'custom.pop.message',
            'target': 'new',
            'context': {'default_name': "Bill Of Materials Successfully Updated"}
        }

class CustomPopMessage(models.Model):
    _name = "custom.pop.message"

    name = fields.Char('Success')






