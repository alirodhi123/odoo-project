from odoo import api, fields, models, _

class manufacturing_order(models.Model):
    _inherit = 'mrp.production'

    is_responsible = fields.Boolean(default=False)
    x_type_mo = fields.Selection(
        [('stc', 'Sticker'), ('ink', 'Tinta Campuran'), ('plate', 'Plate'), ('diecut', 'Diecut')], string='Type MO',
        required=True)


    @api.multi
    def popup_message_pr(self):

        for row in self:
            order_kerja = row.name
            product = row.product_id.id

        return {
            'name': 'Create Purchase Request',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'x.pop.message.pr',
            'target': 'new',
            'context': {
                'default_name': "Are you sure want to create Purchase Request ?",
                'default_x_product_ok': product,
            }
        }

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

