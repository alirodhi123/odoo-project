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


    # Function untuk flagging create PR
    @api.model
    def create(self, vals):

        res = super(purchase_request_inherit, self).create(vals)

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







