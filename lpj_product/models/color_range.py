from odoo import models, fields, api

class Color_Range(models.Model):
    _name = 'x.color.range.pde'
    _inherit = 'mail.thread'

    name = fields.Char(string="No.CR", readonly=True)
    x_product_id = fields.Many2one('product.template', 'Product', readonly=True)
    x_production_id = fields.Many2one('mrp.production', 'Manufacture Order', readonly=True)

    no_OK = fields.Char(related='x_production_id.name', string="No.OK", readonly=True)
    x_state = fields.Selection([
        ('plan', 'Planned'),
        ('produksi', 'Produksi'),
        ('approval', 'Approval Customer'),
        ('done', 'Done'),
        ('cancel', 'Cancel')] , track_visibility='onchange', string="Status CR" , readonly=True)

    x_arah_roll = fields.Char(string = 'Arah Roll', related='x_product_id.x_roll_direction.name',readonly = True)
    x_arah_roll_image = fields.Binary(string = 'Imange Roll', related='x_product_id.x_roll_direction.x_image',readonly = True)
    x_id_core = fields.Char(string = 'ID Core' , track_visibility = 'onchange')

    x_material_cr = fields.Text(string='Material', compute = 'create_color_range')
    x_color = fields.Text(string='Colour' , track_visibility = 'onchange')
    x_sales = fields.Many2one('hr.employee', string = 'Sales' , domain = [('department_id', '=','MKT')] , track_visibility = 'onchange')
    x_article = fields.Char(string = 'Article', compute = 'create_color_range')
    x_design_ref = fields.Char(string='Design Ref. No.', related='x_product_id.x_drawing.name')

    # Daftar Finishing
    x_full_varnish = fields.Boolean(string='Full Varnish Glossy / Matt')
    x_dripp_off = fields.Boolean(string='Dripp Off')
    x_hotprint = fields.Boolean(string='Hotprint')
    x_spot_varnish = fields.Boolean(string='Spot Varnish Glossy / Matt')
    x_laminating = fields.Boolean(string='Laminating OPP')

    x_history_peminjaman = fields.One2many('x.peminjaman.cr','x_cr_ids',string='History Peminjaman' , track_visibility = 'onchange')

    # x_customer = fields.Char(related='x_production_id.order.partner_id.name', string='Customer', readonly=True)
    x_customer = fields.Char(related='x_product_id.x_customer.display_name', string='Customer', readonly=True)
    x_tgl_approval_cr = fields.Datetime("Tanggal di Approval")
    x_jumlah_kembali = fields.Integer("Jumlah Kembali dari Customer")
    x_jumlah_permintaan = fields.Integer("Jumlah Permintaan CR")


    @api.multi
    def create_color_range(self):
        raw_material = ''
        cnt = 0
        material_type_ids = self.x_product_id.x_material_type_ids

        if material_type_ids:
            for data in material_type_ids:
                cnt = cnt + 1
                raw_material = raw_material + str(cnt) + '. ' + data.name.name + '\n'
            self.x_material_cr = raw_material
            self.x_article = self.x_product_id.default_code + ' - ' + self.x_product_id.name


    @api.multi
    def action_cr(self):
        if self.x_state == 'plan':
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
            self.write({'x_state': 'plan'})

    @api.multi
    def action_cancel(self):
        if self.x_state == 'cancel':
            self.write({'x_state': 'plan'})
        else:
            self.write({'x_state': 'cancel'})


class Color_Range_Peminjaman(models.Model):
    _name = 'x.peminjaman.cr'

    name = fields.Char('Peminjam')
    x_peminjam = fields.Many2one('hr.employee', string = 'Sales' , domain = [('department_id', '=','MKT')])
    x_tgl_pinjam = fields.Datetime('Tanggal Peminjaman')
    x_tgl_kembali = fields.Datetime('Tanggal Kembali')
    x_jumlah = fields.Integer('Jumlah')
    x_cr_ids = fields.Many2one('x.color.range.pde','Nomor CR')






