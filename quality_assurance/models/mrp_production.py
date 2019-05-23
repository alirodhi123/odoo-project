# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, exceptions
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError


class mrp(models.Model):
    _inherit = "mrp.production"

    @api.multi
    def generate_quality_alert(self):
        '''
        This function generates quality alerts for the products mentioned in move_lines of given picking and also have quality measures configured.
        '''
        quality_alert = self.env['quality.alert']
        quality_measure = self.env['quality.measure']
        for move in self.move_finished_ids:
            measures = quality_measure.search([('product_id', '=', move.product_id.id), ('trigger_time', 'in', self.picking_type_id.id)])
            if measures:
                quality_alert.create({
                    'name': self.env['ir.sequence'].next_by_code('quality.alert') or _('New'),
                    'product_id': move.product_id.id,
                    'picking_id_mrp': self.id,
                    'origin': self.name,
                })
            else:
                self.generate_quality_measure()

    # Fungsi dijalankan ketika master quality measure tidak ada
    @api.multi
    def generate_quality_measure(self):
        # Get sequence untuk quality measure
        prefix = "QC-"
        product_product = self.env['product.product']
        product = product_product.search([('id', '=', self.product_id.id)])
        default_code = product.default_code # Get internal code di product

        # Create quality measure jika tidak ada pada master quality measure
        quality_measure = self.env['quality.measure']

        for move in self.move_finished_ids:
            measures = quality_measure.search([('product_id', '=', move.product_id.id), ('trigger_time', 'in', self.picking_type_id.id)])
            if not measures:
                quality_measure.create({
                    'name': prefix + default_code,
                    'product_id': move.product_id.id,
                    'type': 'quality',
                    'trigger_time': [[6, 0, [6]]] #create IDS (6, 0, [ID of one2many]) for many2many
                })
                # Setelah create quality measure, diarahkan kembali ke method quality_alert dan create quality alert
                self.generate_quality_alert()

    # Button Create Work Order
    @api.multi
    def button_plan(self):
        if self.alert_count == 0:
            self.generate_quality_alert()
        res = super(mrp, self).button_plan()
        return res


    @api.depends('move_finished_ids')
    def _compute_alert(self):
        '''
        This function computes the number of quality alerts generated from given picking.
        '''
        for picking in self:
            alerts = self.env['quality.alert'].search([('picking_id_mrp', '=', picking.id)])
            picking.alert_ids = alerts
            picking.alert_count = len(alerts)

    @api.multi
    def quality_alert_action(self):
        '''
        This function returns an action that display existing quality alerts generated from a given picking.
        '''
        action = self.env.ref('quality_assurance.quality_alert_action')
        result = action.read()[0]

        # override the context to get rid of the default filtering on picking type
        result.pop('id', None)
        result['context'] = {}
        alert_ids = sum([picking.alert_ids.ids for picking in self], [])
        # choose the view_mode accordingly
        if len(alert_ids) > 1:
            result['domain'] = "[('id','in',[" + ','.join(map(str, alert_ids)) + "])]"
        elif len(alert_ids) == 1:
            res = self.env.ref('quality_assurance.quality_alert_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = alert_ids and alert_ids[0] or False
        return result

    alert_count = fields.Integer(compute='_compute_alert', string='Quality Alerts', default=0)
    alert_ids = fields.Many2many('quality.alert', compute='_compute_alert', string='Quality Alerts', copy=False)



