from odoo import api, fields, models
from odoo import tools


class assets_helpdesk(models.Model):
    _name = 'asset.helpdesk'

    asset_number = fields.Char('Asset Number', size=64)
    name = fields.Char('Asset Name', required=True, translate=True)
    stock_asset = fields.Integer('Quantity')
    description = fields.Text('Description')
    user_id = fields.Many2one('res.users', 'Assigned to', track_visibility='onchange')
    active = fields.Boolean('Active', default=True)

    # info field
    model = fields.Char('Model', size=64)
    serial = fields.Char('Serial no.', size=64)

    # vendor_id = fields.Many2one('res.partner', 'Vendor')
    # manufacturer_id = fields.Many2one('res.partner', 'Manufacturer')
    # start_date = fields.Date('Start Date')
    # purchase_date = fields.Date('Purchase Date')
    # warranty_start_date = fields.Date('Warranty Start')
    # warranty_end_date = fields.Date('Warranty End')
    image = fields.Binary("Image")
    image_small = fields.Binary("Small-sized image")
    image_medium = fields.Binary("Medium-sized image")

    # category_ids = fields.One2many('asset.helpdesk.category', id1='asset_id', id2='category_id', string='Tags')


    # insert new record
    @api.model
    def create(self, vals):
        tools.image_resize_images(vals)
        return super(assets_helpdesk, self).create(vals)

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)
        return super(assets_helpdesk, self).write(vals)


class assets_helpdesk_category(models.Model):
    _description = 'Asset Tags'
    _name = 'asset.helpdesk.category'

    name = fields.Char('Tag', required=True, translate=True)
    # asset_ids = fields.Many2many('asset.helpdesk', id1='category_id', id2='asset_id', string='Assets')
