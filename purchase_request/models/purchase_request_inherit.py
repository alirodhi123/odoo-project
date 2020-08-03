from mock.mock import self

from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, time


class purchase_request_inherit(models.Model):
    _inherit = 'purchase.request'

    # get active_id for the tree
    def _default_mrp_production(self):
        return self.env['mrp.production'].browse(self._context.get('active_id'))

    x_no_ok = fields.Many2one('mrp.production', string="Order Kerja")
    x_bom = fields.Many2one('mrp.production')
    x_product = fields.Char(string="Product")

    # Tambahan no-SO -Uswa
    x_no_so = fields.Many2one('sale.order', string="SO Number")


    # Function untuk flagging create PR
    @api.model
    def create(self, vals):

        # kasi if else

        res = super(purchase_request_inherit, self).create(vals)

        order_number = vals['x_no_so']

        if order_number:
            # Tambahan PR SO -Uswa

            # select from table berdasarkan id
            purchase_request = self.env['sale.order'].search([('id', '=', order_number)])
            # write di is_responsible
            purchase_request.write({'is_responsible': True})

            # Automatically filled in line_ids sales order
            terms_obj = self.env['sale.order']
            terms = []
            termsids = terms_obj.search([('id', '=', order_number)])
            if termsids:
                for rec in termsids.order_line:
                    values = {}
                    values['product_id'] = rec.product_id
                    values['name'] = rec.product_id.name
                    values['product_uom_id'] = rec.product_uom
                    values['product_qty'] = rec.product_uom_qty
                    terms.append((0, 0, values))

                res.update({'line_ids': terms})

        else:
            order_kerja = vals['x_no_ok']

            purchase_request = self.env['mrp.production'].search([('id', '=', order_kerja)])
            purchase_request.write({'is_responsible': True})

            # Automatically filled in line_ids
            terms_obj = self.env['mrp.production']
            terms = []
            termsids = terms_obj.search([('id', '=', order_kerja)])
            if termsids:
                for rec in termsids.move_raw_ids:
                    values = {}
                    values['product_id'] = rec.product_id
                    values['name'] = rec.product_id.name
                    values['product_uom_id'] = rec.product_uom
                    terms.append((0, 0, values))

                res.update({'line_ids': terms})

        return res


class purchase_request_line(models.Model):
    _inherit = 'purchase.request.line'



    bom_line_ids = fields.Many2one('mrp.bom.line', string="Product")
    catatan_barang = fields.Text(string="Notes")







