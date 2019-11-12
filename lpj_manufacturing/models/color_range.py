from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api


class CreateOK_msr(models.Model):
    _inherit = 'mrp.production'

    x_color_range_ids = fields.One2many('x.color.range.pde', 'x_production_id', 'Color Range', copy=False,
                                        readonly=True)
    x_color_range_name = fields.Many2one('x.color.range.pde', compute='_get_cr', string='Nomor CR', readonly=True)
    x_cek_cr = fields.Boolean(string='Centang CR', compute='_centang_cr')

    # @api.onchange('product_tmpl_id.x_reg_cr_pde_m')
    # @api.multi
    @api.onchange('product_tmpl_id.x_reg_cr_pde_m', 'product_tmpl_id.x_reg_cr_mkt_m', 'product_id')
    def _centang_cr(self):

        if self.product_tmpl_id.x_reg_cr_mkt_m and self.product_tmpl_id.x_reg_cr_pde_m:
            self.x_cek_cr = True
        else:
            self.x_cek_cr = False

    @api.multi
    def btn_color_range(self):
        colorrange = self.product_id.env['x.color.range.pde']

        colorrange.env.cr.execute(
            'select x_production_id, name from x_color_range_pde where x_production_id =' + str(self.id))
        data_baru = colorrange.env.cr.fetchone()

        self.product_tmpl_id.x_reg_cr_pde_m = False
        sum_req_cr = self.product_tmpl_id.x_jumlah_cr_pde_m

        if data_baru:
            colorrange.update({
                'no_OK': self.name,
                'x_product_id': self.product_id.product_tmpl_id.id,
                'x_production_id': self.id,
            })
            return {
                'name': 'Update Color Range',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'pop.message.lock.ok',
                'target': 'new',
                'context': {
                    'default_name': "Nomor OK : " + self.name,
                    'default_name_second': "Nomor CR : " + data_baru[1]
                }
            }
        else:
            sequence = self.env['ir.sequence'].next_by_code('sequence.cr') or ('New')
            colorrange.create({
                'name': sequence,
                'no_OK': self.name,
                'x_product_id': self.product_id.product_tmpl_id.id,
                'x_state': 'plan',
                'x_production_id': self.id,
                'x_jumlah_permintaan': sum_req_cr
            })

            return {
                'name': 'Create Color Range',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'pop.message.lock.ok',
                'target': 'new',
                'context': {
                    'default_name': "Nomor OK : " + self.name,
                    'default_name_second': "Nomor CR : " + sequence
                }
            }

    @api.multi
    @api.depends('x_color_range_ids')
    def _get_cr(self):
        if self.x_color_range_ids:
            self.x_color_range_name = self.x_color_range_ids
        else:
            self.x_color_range_name = ''


