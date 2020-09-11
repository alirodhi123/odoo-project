from odoo import api, fields, models
from odoo import tools


class assets_helpdesk(models.Model):
    _name = 'asset.helpdesk'

    name = fields.Char(string='Asset Name', track_visibility='always', required=True)
    kategori_asset = fields.Selection([('computer', 'Computer'),
                                        ('monitor', 'Monitor'),
                                        ('printer', 'Printer'),
                                        ('catridges', 'Catridges'),
                                        ('ups', 'UPS'),
                                        ('router', 'Router'),
                                        ('telephon', 'Telephon'),
                                        ('keyboard&mouse', 'Keyboard & Mouse')], string="Category Assets")

    user_id = fields.Many2one('res.users', 'Assigned to', track_visibility='onchange')
    user_dept_id = fields.Many2one('hr.department', 'Department Group', track_visibility='onchange')

    status_asset = fields.Selection([('archived', 'Archived'),
                                    ('available', 'Available'),
                                    ('inuse', 'In Use')], string="Status")
    tipe_asset = fields.Char('Type')
    manufaktur_asset = fields.Char('Manufacturer')
    model_asset = fields.Char('Model')
    serial_number = fields.Char('Serial Number')

    technician_id = fields.Many2one('res.users', 'Technician', track_visibility='onchange')
    technician_dept_id = fields.Many2one('hr.department', 'Technician Dept', track_visibility='onchange')
    tgl_kedatangan_asset = fields.Datetime(string=' Asset Arrival Date', track_visibility='onchange')
    description = fields.Text(string=' Description')

    image = fields.Binary("Image")
    image_small = fields.Binary("Small-sized image")
    image_medium = fields.Binary("Medium-sized image")

    ticket_assethelpdesk_count = fields.Integer(string="Ticket Helpdesk", compute='_ticket_asset_helpdesk_count')


    # insert new record
    @api.model
    def create(self, vals):
        tools.image_resize_images(vals)
        return super(assets_helpdesk, self).create(vals)

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)
        return super(assets_helpdesk, self).write(vals)


    # uswa- tambah ini untuk toggle butoon di form asset helpdesk
    @api.multi
    def action_view_ticket_asset_helpdesk(self):
        action = self.env.ref('helpdesk_lite.helpdesk_ticket_categ_act0').read()[0]
        action['domain'] = [('assets_helpdesk_ids', '=', self.ids)]
        action['context'] = {}
        return action

    @api.multi
    def _ticket_asset_helpdesk_count(self):
        hasil = 0
        for o in self:
            ticket_count_obj = self.env['helpdesk_lite.ticket'].search([('assets_helpdesk_ids', '=', o.id)])
            if ticket_count_obj.ids:
                # hasil += 1
                hasil = len(ticket_count_obj.ids)

            o.ticket_assethelpdesk_count = hasil
    # uswa- end


# class assets_helpdesk_category(models.Model):
#     _description = 'Asset Category'
#     _name = 'asset.helpdesk.category'
#
#     name = fields.Char('Tag', required=True, translate=True)
#     # asset_ids = fields.Many2many('asset.helpdesk', id1='category_id', id2='asset_id', string='Assets')

