from odoo import api, fields, models, _

class manufacturing_order(models.Model):
    _inherit = 'mrp.production'

    is_responsible = fields.Boolean(default=False)

    # Fungsi button create PR
    # Fungsi mengirim data pada object lain
    @api.multi
    def open_second_class(self):
        ac = self.env['ir.model.data'].xmlid_to_res_id('purchase_request.view_purchase_request_form', raise_if_not_found=True)
        for o in self:
            order_kerja = o.name

            for line in o.move_raw_ids:
                product = line.product_id.name

        result = {
            'name': 'Create PR',
            'view_type': 'form',
            'res_model': 'purchase.request',
            'view_id': ac,
            'context': {

            },
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'current',
        }
        return result