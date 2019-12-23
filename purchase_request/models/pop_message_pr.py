from odoo import api, fields, models, _



class pop_message_pr(models.Model):
    _name = 'x.pop.message.pr'

    def _default_id(self):
         return self.env['mrp.production'].browse(self._context.get('active_id'))

    name = fields.Char(readonly=True)
    x_no_ok = fields.Many2one('mrp.production', string="Order Kerja", readonly=True, default=_default_id)
    x_product_ok = fields.Many2one('product.product', string="Product", readonly=True)


    @api.multi
    def create_pr(self):
        ac = self.env['ir.model.data'].xmlid_to_res_id('purchase_request.view_purchase_request_form',
                                                       raise_if_not_found=True)
        for row in self:
            order_kerja = row.x_no_ok
            for data in order_kerja:
                no_ok = data.id

        result = {
            'name': 'Create PR',
            'view_type': 'form',
            'res_model': 'purchase.request',
            'view_id': ac,
            'context': {
                'default_x_no_ok': no_ok
            },
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'current',
        }
        return result

    @api.multi
    def dont_need_pr(self):
        id = self.x_no_ok.id

        order_kerja = self.env['mrp.production'].search([('id', '=', id)])
        if order_kerja:
            order_kerja.write({'is_responsible': True})