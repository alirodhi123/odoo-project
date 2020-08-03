from odoo import api, fields, models, _

class efaktur(models.Model):
    _name = 'vit.efaktur'

    name = fields.Char("eFaktur Number")
    year = fields.Integer(string="Year", required=False, )

    invoice_ids = fields.One2many(comodel_name="account.invoice",
                                  inverse_name="efaktur_id",
                                  string="Invoices", required=False, )

    @api.depends('invoice_ids')
    def _used(self):
        for efaktur in self:
            if efaktur.invoice_ids:
                efaktur.is_used = True
            else:
                efaktur.is_used = False


    is_used = fields.Boolean(string="Is Used", compute="_used", store=True )
