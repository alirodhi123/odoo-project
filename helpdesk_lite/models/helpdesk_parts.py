from odoo import api, fields, models
from odoo import tools


# line obj buat parts
class parts_helpdesk_line(models.Model):
    _name = 'parts.helpdesk.line'


# uswa-tambah field ini buat page='Parts'
    helpdesk_parts_id = fields.Many2one('helpdesk_lite.ticket')

    parts2_id = fields.Many2one('product.product', string="Parts", required=True)
    parts_desc = fields.Text(string="Description")
    parts_qty = fields.Float(string="Quantity")
    parts_uom = fields.Many2one('product.uom', string="Unit of Measure", required=True)

    @api.onchange('parts2_id')
    def onchange_parts(self):
        self.parts_uom = self.parts2_id.uom_id.id

    @api.model
    def create(self, values):
        ids = self.search([('parts2_id','=',values['parts2_id'])])
        if len(ids)>0:
            values['parts_qty'] = ids[0].parts_qty + values['parts_qty']
            ids[0].write(values)
            return ids[0]
        # ids = self.search([('maintenance_id','=',False)])
        # if len(ids)>0:
        #     ids[0].write(values)
        #     return ids[0]
        return super(parts_helpdesk_line, self).create(values)


