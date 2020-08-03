from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



class register_payment_inherit(models.TransientModel):
    _inherit = 'account.register.payments'

    x_draft_payment = fields.Many2one('x.register.payment', string="Draft Payment")

    @api.model
    def default_get(self, fields):
        res = super(register_payment_inherit, self).default_get(fields)

        terms = []
        invoice_obj = self.env['account.invoice']
        invoice_ids = self.env.context.get('active_ids', False)
        invoice = invoice_obj.browse(invoice_ids)

        for row in invoice:
            draft_payment = row.x_custom_payment_id.id

        res.update({
            'x_draft_payment' : draft_payment
        })

        return res

    # Fungsi update flagging draft payment ketika sudah paid
    @api.multi
    def paid_draft_payment_wizard(self):
        draft_pay = self.x_draft_payment

        invoice_obj = self.env['x.register.payment'].search([('id', '=', draft_pay.id)])
        if invoice_obj:
            invoice_obj.write({'x_flag_paid': True})

    # INHERITE FUNCTION VALIDATE PAYMENT WIZARD
    @api.multi
    def create_payment(self):
        # FUNCTION UPDATE PLAFON
        self.paid_draft_payment_wizard()

        res = super(register_payment_inherit, self).create_payment()
        return res