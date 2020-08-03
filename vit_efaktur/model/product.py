from odoo import api, fields, models, _

class product(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    is_efaktur_exported = fields.Boolean(string="Is eFaktur Exported",  )
    date_efaktur_exported = fields.Datetime(string="eFaktur Exported Date", required=False, )

