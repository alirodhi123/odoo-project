from odoo import models, fields, api
from datetime import datetime


class PopUpProduction(models.Model):
    _name = 'x.popup.production'

    x_popup_production_ids = fields.One2many('x.popup.production.line', 'x_popup_production_id')
    x_count_data = fields.Integer(compute='_compute_line_count', string="Jumlah OK")

    @api.model
    def default_get(self, fields):
        res = super(PopUpProduction, self).default_get(fields)
        terms = []

        hr_attendance = self.env['hr.attendance']
        manufacturing_obj = self.env['mrp.production']
        manufacturing_ids = self.env.context.get('active_ids', False)

        manufacturing = manufacturing_obj.browse(manufacturing_ids)

        for row in manufacturing:
            values = {}

            id = row.id
            product = row.product_id.id
            qty = row.product_qty
            uom = row.product_uom_id.name
            source = row.origin

            values['x_manufacturing_id'] = id
            values['x_product_production'] = product
            values['x_qty_production'] = qty
            values['x_uom_production'] = uom
            values['x_source_production'] = source

            terms.append((0, 0, values))
            res['x_popup_production_ids'] = terms

        return res

    # Function menghitung jumlah OK yang akan di turunkan di produksi
    @api.depends('x_popup_production_ids')
    def _compute_line_count(self):
        self.x_count_data = len(self.mapped('x_popup_production_ids'))

    @api.multi
    def send_to_produksi(self):
        for manufacturing in self:
            default = datetime.now().strftime('%Y-%m-%d')
            mrp = manufacturing.env['mrp.production']
            manufacturing_obj = manufacturing.x_popup_production_ids

            for row in manufacturing_obj:
                no_ok = row.x_manufacturing_id.id

                cek = mrp.search([('id', '=', no_ok)])
                if cek:
                    cek.write({
                        'x_tgl_produksi': default,
                        'x_flag_produksi': True
                    })




class PopUpProductionLine(models.Model):
    _name = 'x.popup.production.line'

    x_manufacturing_id = fields.Many2one('mrp.production', string="No OK", readonly=True)
    x_popup_production_id = fields.Many2one('x.popup.production')
    x_product_production = fields.Many2one('product.product', string="Product", readonly=True)
    x_qty_production = fields.Float(string="Qty OK", readonly=True)
    x_uom_production = fields.Char(string="Unit of Measure", readonly=True)
    x_source_production = fields.Char(string="Source", readonly=True)
