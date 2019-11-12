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

    # Fungsi parsing data to other view
    @api.multi
    def create_ok(self):
         ac = self.env['ir.model.data'].xmlid_to_res_id('mrp.mrp_production_form_view', raise_if_not_found=True)

         for o in self:
              order_id = o.x_sale_order.id
              order_name = o.x_sale_order.name
              product = o.x_sale_order_line.id
              toleransi = o.x_sale_order_line.x_toleransi
              due_date_kirim = o.x_sale_order_line.x_duedate_kirim

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
                   'default_x_due_kirim': due_date_kirim
              },
              'type': 'ir.actions.act_window',
              'view_mode': 'form'
         }
         return result

    @api.multi
    def dont_need_ok(self):
        sale_order_id = self.x_sale_order
        sale_order_line_id = self.x_sale_order_line

        sale_order = self.env['sale.order'].search([('id', '=', sale_order_id.id)])
        if sale_order:
            for row in sale_order.order_line:
                sale_order_line = self.env['sale.order.line'].search([('id', '=', sale_order_line_id.id)])
                if sale_order_line:
                    return sale_order_line.update({'x_flag_mo': True})

class PopMessageLockOk(models.Model):
    _name = 'pop.message.lock.ok'

    name = fields.Char()
    name_second = fields.Char()


