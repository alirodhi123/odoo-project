from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from datetime import datetime
from odoo.exceptions import UserError


class MessageBlock(models.Model):
    _name = 'message.block.pengiriman'

    name = fields.Char()
    name_second = fields.Char()