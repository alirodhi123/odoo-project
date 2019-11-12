from odoo import models, fields, api

class Color_Range(models.Model):
    _name = 'x.color.range'
    _inherit = 'mail.thread'

    name = fields.Char(string="No.CR", readonly=True)
    no_OK = fields.Char(related='x_production_id.name', string="No.OK", readonly=True)
    x_state = fields.Selection([
        ('qa', 'QA'),
        ('produksi', 'Produksi'),
        ('approval', 'Approval Customer'),
        ('done', 'Done'),
        ('cancel', 'Cancel')] , track_visibility='onchange', string="Status CR" , readonly=True)

    x_production_id = fields.Many2one('mrp.production', 'Nomor OK',readonly=True)

    # x_arah_roll = fields.Char(related='x_production_id.product_id.x_roll_direction.name', string = 'Arah Roll',readonly = True)
    x_arah_roll = fields.Char(string = 'Arah Roll', compute='create_color_range',readonly=True)
    x_arah_roll_image = fields.Binary(string = 'Imange Roll', compute='create_color_range',readonly=True)
    x_id_core = fields.Char(string = 'ID Core')
    x_customer = fields.Char(related='x_production_id.order.partner_id.name',string='Customer',readonly = True)
    x_material_cr = fields.Text(string='Material', compute = 'create_color_range')
    x_material = fields.One2many('x.material.type',string='Material')
    x_color = fields.Text(string='Colour')
    x_sales = fields.Many2one('hr.employee', string = 'Sales' , domain = [('department_id', '=','MKT')])
    # x_material = fields.One2many('mrp.production',related='x_production_id.product_id.x_material_type_ids',string='Material')
    x_article = fields.Char(string = 'Article', compute = 'create_color_range')
    x_design_ref = fields.Char(string='Article', compute='create_color_range')

    # Daftar Finishing
    x_full_varnish = fields.Boolean(string='Full Varnish Glossy / Matt', track_visibility='onchange')
    x_dripp_off = fields.Boolean(string='Dripp Off', track_visibility='onchange')
    x_hotprint = fields.Boolean(string='Hotprint', track_visibility='onchange')
    x_spot_varnish = fields.Boolean(string='Spot Varnish Glossy / Matt', track_visibility='onchange')
    x_laminating = fields.Boolean(string='Laminating OPP', track_visibility='onchange')
    # related = "x_production_id.x_product_id",

    @api.multi
    def create_color_range(self):
        self.x_arah_roll = self.x_production_id.product_id.x_roll_direction.name
        self.x_arah_roll_image = self.x_production_id.product_id.x_roll_direction.x_image
        # self.x_material = self.x_production_id.product_id.x_material_type_ids
        raw_material=''
        cnt=0
        for data in self.x_production_id.product_id.x_material_type_ids:
            cnt=cnt+1
            raw_material = raw_material + str(cnt) +'. '+ data.name.name + '\n'
        self.x_material_cr=raw_material
        self.x_article = self.x_production_id.product_id.default_code + ' - ' + self.x_production_id.product_id.name
        self.x_design_ref = self.x_production_id.product_id.x_drawing.name


    @api.multi
    def action_cr(self):
        if self.x_state == 'qa':
            self.write({'x_state': 'produksi'})
        elif self.x_state == 'produksi':
            self.write({'x_state': 'approval'})
        elif self.x_state == 'approval':
            self.write({'x_state': 'done'})

    @api.multi
    def action_kembali(self):
        if self.x_state == 'done':
            self.write({'x_state': 'approval'})
        elif self.x_state == 'approval':
            self.write({'x_state': 'produksi'})
        elif self.x_state == 'produksi':
            self.write({'x_state': 'qa'})

    @api.multi
    def action_cancel(self):
        if self.x_state == 'cancel':
            self.write({'x_state': 'qa'})
        else:
            self.write({'x_state': 'cancel'})




