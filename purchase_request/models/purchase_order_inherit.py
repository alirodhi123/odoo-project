# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp

_STATES = [
    ('ibsb', 'Item Baru - Supplier Baru'),
    ('ibsl', 'Item Baru - Supplier Lama'),
    ('ilsb', 'Item Lama - Supplier Baru'),
    ('ilsl', 'Item Lama - Supplier Lama')
]

# class PurchaseOrderInhetir(models.Model):
#     _inherit = 'purchase.order'
#
#     x_category_purchase = fields.Selection(selection=_STATES,
#                              string='Purchase Category',
#                              track_visibility='onchange',
#                              default='ibsb')

class PurchaseOrderInhetir(models.Model):
    _inherit = 'purchase.order.line'

    x_category_purchase = fields.Selection(selection=_STATES,
                             string='Product Category',
                             track_visibility='onchange',default='ilsl')


