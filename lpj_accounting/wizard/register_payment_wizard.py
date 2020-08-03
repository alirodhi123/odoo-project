from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError, ValidationError


class wizard_register_payment(models.Model):
    _name = 'x.popup.register.payment'

    x_vendor_wizard = fields.Many2one('res.partner', string="Vendor")
    x_wizard_register_payment_line = fields.One2many('x.popup.register.payment.line', 'x_register_payment_id')

    @api.model
    def default_get(self, fields):
        res = super(wizard_register_payment, self).default_get(fields)
        terms = []

        invoice_obj = self.env['account.invoice']
        invoice_ids = self.env.context.get('active_ids', False)
        invoice = invoice_obj.browse(invoice_ids)

        for row in invoice:
            values = {}
            id = row.id
            vendor = row.partner_id
            name = row.name
            origin = row.origin
            untaxed_amount = row.amount_untaxed
            tax = row.amount_tax
            total = row.amount_total
            bill_date = row.date_invoice
            due_date = row.date_due

            # Cek invoice
            if row.state != 'open':
                raise UserError(_("You can only register payments for open invoices"))
            if row.commercial_partner_id != invoice[0].commercial_partner_id:
                raise UserError(_("In order to pay multiple invoices at once, they must belong to the same commercial partner."))
            if row.currency_id != invoice[0].currency_id:
                raise UserError(_("In order to pay multiple invoices at once, they must use the same currency."))

            values['x_account_id'] = id
            values['x_vendor_wizard_line'] = vendor.id
            values['x_origin_wizard_line'] = origin
            values['x_untaxed_amount_wizard_line'] = untaxed_amount
            values['x_tax_wizard_line'] = tax
            values['x_total_wizard_line'] = total
            values['x_bill_date_line'] = bill_date
            values['x_due_date_line'] = due_date

            terms.append((0, 0, values))
            res['x_wizard_register_payment_line'] = terms

        return res

    @api.multi
    def pay_to_draft(self):
        for bill in self:
            terms = []
            ac = bill.env['ir.model.data'].xmlid_to_res_id('lpj_accounting.register_payment_custom_form_view', raise_if_not_found=True)
            payment_wizard_line = bill.x_wizard_register_payment_line

            for row in payment_wizard_line:
                bill_id = row.x_account_id
                vendor = row.x_vendor_wizard_line
                origin = row.x_origin_wizard_line
                bill_date = row.x_bill_date_line
                due_date = row.x_due_date_line
                untaxed_amount = row.x_untaxed_amount_wizard_line
                tax = row.x_tax_wizard_line
                total = row.x_total_wizard_line

                values = {}
                values['x_no_bill'] = bill_id.id
                values['x_account'] = 13
                values['x_origin'] = origin
                values['x_bill_date'] = bill_date
                values['x_due_date'] = due_date
                values['x_untaxed_amount_payment'] = untaxed_amount
                values['x_tax_payment'] = tax
                values['x_total_payment'] = total

                terms.append((0, 0, values))

            result = {
                'name': '2nd class',
                'view_type': 'form',
                'res_model': 'x.register.payment',
                'view_id': ac,
                'context': {
                    'default_x_vendor': vendor.id,
                    'default_x_register_payment_line': terms,
                },
                'type': 'ir.actions.act_window',
                'view_mode': 'form'
            }

            return result


class wizard_register_payment_line(models.Model):
    _name = 'x.popup.register.payment.line'

    x_account_id = fields.Many2one('account.invoice', string="Bill")
    x_register_payment_id = fields.Many2one('x.popup.register.payment', ondelete='cascade')
    currency_id = fields.Many2one('res.currency', store=True, readonly=True)
    x_vendor_wizard_line = fields.Many2one('res.partner', string="Vendor")
    x_origin_wizard_line = fields.Char(string="Source Document")
    x_untaxed_amount_wizard_line = fields.Monetary(string="Untaxed Amount")
    x_tax_wizard_line = fields.Monetary(string="Tax")
    x_total_wizard_line = fields.Monetary(string="Total")
    x_bill_date_line = fields.Date(string="Bill Date")
    x_due_date_line = fields.Date(string="Due Date")


