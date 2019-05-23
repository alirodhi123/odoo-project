from odoo import models, fields, api, _


class res_partner(models.Model):
    _inherit = 'res.partner'

    x_block_customer = fields.Selection([('no', 'Block'), ('yes', 'Open')], default='no', string="Block Customer")

    # Function for update x_block_customer untuk SO
    @api.multi
    def write(self, vals):
        res = super(res_partner, self).write(vals)

        for partner in self:
            partner_name = partner.name
            sale_order = self.env['sale.order'].search(
                [('state', 'in', ['draft', 'sent']), ('partner_id', '=', partner_name)])
            if sale_order:
                for sale_order_new in sale_order:
                    block_customer = partner.x_block_customer
                    if block_customer == 'no':
                        sale_order_new.update({'is_block': 'no'})
                    if block_customer == 'yes':
                        sale_order_new.update({'is_block': 'yes'})
                return res

            else:
                return res
