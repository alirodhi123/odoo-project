from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class PopMessageManufacturing(models.Model):
    _name = "pop.message.ok"

    def _default_id(self):
         return self.env['sale.order.line'].browse(self._context.get('active_id'))

    name = fields.Char()
    x_sale_order = fields.Many2one('sale.order', string="No SO")
    x_sale_order_char = fields.Char(string="No SO")
    x_sale_order_line = fields.Many2one('sale.order.line', string="Product", default=_default_id)
    x_pop_message_ids = fields.One2many('pop.message.ok.line', 'x_pop_message_id', string="BOM List")
    x_reason_dont_need_ok = fields.Text(string="Reason Don't Need OK")

    # Fungsi parsing data to OK
    @api.multi
    def create_ok(self):
         ac = self.env['ir.model.data'].xmlid_to_res_id('mrp.mrp_production_form_view', raise_if_not_found=True)

         for o in self:
              order_id = o.x_sale_order.id
              order_name = o.x_sale_order.name
              product = o.x_sale_order_line.id
              toleransi = o.x_sale_order_line.x_toleransi
              due_date_kirim = o.x_sale_order_line.x_duedate_kirim
              notes = o.x_sale_order.note
              manufactruing_type = o.x_sale_order_line.x_manufacturing_type
              planning_type = o.x_sale_order_line.x_planning_type

         result = {
              'name': '2nd class',
              'view_type': 'form',
              'res_model': 'mrp.production',
              'view_id': ac,
              'context': {
                   'default_order': order_id,
                   'default_origin': order_name,
                   'default_x_product_order_line': product,
                   'default_x_toleransi': toleransi,
                   'default_x_due_kirim': due_date_kirim,
                   'default_x_note_so': notes,
                   'default_x_manufacturing_type_ok': manufactruing_type,
                   'default_x_planning_type_ok': planning_type,
              },
              'type': 'ir.actions.act_window',
              'view_mode': 'form'
         }
         return result

    # Fungsi dont need OK
    @api.multi
    def dont_need_ok(self):
        for data in self:
            sale_order_id = data.x_sale_order
            sale_order_line_id = data.x_sale_order_line
            reason_dont_need = data.x_reason_dont_need_ok

            sale_order = data.env['sale.order'].search([('id', '=', sale_order_id.id)])
            if sale_order:
                for row in sale_order.order_line:
                    sale_order_line = data.env['sale.order.line'].search([('id', '=', sale_order_line_id.id)])
                    if sale_order_line:
                        return sale_order_line.update({
                            'x_flag_mo': True,
                            'x_reason_dont_need_ok': reason_dont_need,
                        })


class PopMessageManufacturingLine(models.Model):
    _name = 'pop.message.ok.line'

    x_pop_message_id = fields.Many2one('pop.message.ok', ondelete='cascade')
    product_text = fields.Text(string="Product")
    reference_text = fields.Char(string="Reference")



class PopMessageLockOk(models.Model):
    _name = 'pop.message.lock.ok'

    name = fields.Char()
    name_second = fields.Char()


