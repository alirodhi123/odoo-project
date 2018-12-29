# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class technical_data(models.Model):
    _name = 'x.tds'
    _inherit = 'mail.thread'
    # _description = 'Test untuk drawing'

    name = fields.Char(string='Code')

    x_file = fields.Binary( 'Sample Cetak', track_visibility='onchange')
    #x_machine = fields.Many2one('mrp.workcenter', 'Machine')
    x_operator = fields.Char('Operator',track_visibility='onchange')
    x_diecut_type = fields.Many2one('x.diecut.type','Diecut Type',track_visibility='onchange')
    x_plate_type = fields.Many2one('x.plate.type','Plate Type',track_visibility='onchange')
    x_speed = fields.Float('Speed(MPM)',track_visibility='onchange')
    x_corona = fields.Float('Corona(Watt)',track_visibility='onchange')
    x_tension_unwind = fields.Float('Tension Unwind(Newton)',track_visibility='onchange')
    x_tension_rewind = fields.Float('Tension Rewind(Newton)',track_visibility='onchange')
    x_tension_core_unwind = fields.Float('Tension Core Unwind(Newton)',track_visibility='onchange')
    x_tooth_number = fields.Float('Tooth Number',track_visibility='onchange')
    x_material = fields.Many2one('product.template','Material',track_visibility='onchange')
    x_mounting_tape = fields.Char('Mounting Tape',track_visibility='onchange')
    x_description = fields.Char(string='description', track_visibility='onchange')
    x_tds_line = fields.One2many('x.tds.line','x_tds_ids','Detail',track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('x.tds') or _('New')

        result = super(technical_data, self).create(vals)
        return result

class technical_data_line(models.Model):
    _name = 'x.tds.line'
    _inherit = 'mail.thread'

    x_unit = fields.Integer('Unit',track_visibility='onchange')
    x_warna = fields.Many2one('product.template',string='Warna',domain=[('categ_id', '=', 13)],track_visibility='onchange')
    x_anylox = fields.Float('Anylox',track_visibility='onchange')
    x_bcm = fields.Char('BCM',track_visibility='onchange')
    x_description = fields.Char('Keterangan',track_visibility='onchange')
    x_tds_ids = fields.Many2one('x.tds')




