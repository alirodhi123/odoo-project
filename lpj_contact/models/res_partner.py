from odoo import models, fields, api, _


class res_partner(models.Model):
    _inherit = 'res.partner'

    x_block_customer = fields.Selection([('no', 'Block'), ('yes', 'Open')], default='no', string="Block Customer")
    x_toleransi_pengiriman = fields.Float(string="Toleransi Pengiriman %")
    is_mkt = fields.Boolean(string="check mkt", compute="is_mkt_act")
    is_administrator = fields.Boolean(string="Check Admin", compute='is_admin_act')
    x_company_size = fields.Selection([('s', 'Small (0-50 person)'), ('m', 'Medium (50-250 person)'), ('l', 'Large (>250 person)')], string='Company Size')
    x_avg_kebutuhan = fields.Selection(
        [('s', 'Small (< Rp.100jt/th)'), ('m', 'Medium (Rp.100jt-Rp.500jt/th)'), ('l', 'Large (Rp.500jt-Rp.2M/th)')
            , ('xl', 'X-Large (>Rp.2M/th)')],
        string='Avg Kebutuhan Label', required = True)
    x_priority = fields.Selection([
        ('0', 'Very Low'),
        ('1', 'Low'),
        ('2', 'Medium'),
        ('3', 'High'),
        ('4', 'Very High'),
        ('5', 'Superuser')],
        string='Priority')
    x_status = fields.Selection([
        ('New', 'New'),
        ('Existing', 'Existing')],
        string='Status Customer', default = 'New')
    x_industry = fields.Selection([
        ('food', 'Food and Beverage'),
        ('healthy', 'Farmasi and Healthcare'),
        ('goverment', 'Goverment / Military / Education'),
        ('pariwisata', 'Pariwisata'),
        ('garment', 'Garment'),
        ('huseware', 'Huseware'),
        ('personalcare', 'Personal Care'),
        ('tambang', 'Tambang / Chemical'),
        ('manufacturing', 'Manufacturing / Export Import'),
        ('technology', 'Technology'),
        ('cargo', 'Cargo / Pengiriman')], default='food', string="Bidang Industri", required=True)
    x_jumlah_karyawan = fields.Selection([
        ('less', '< 100 Karyawan'),
        ('small', '100 - 300 Karyawan'),
        ('medium', '301 - 500 Karyawan'),
        ('large', '501 - 1000 Karyawan'),
        ('too_much', '> 1000 Karyawan')], default='less', string="Jumlah Karyawan")
    jalan = fields.Char(string="Jalan")
    x_block_pengiriman = fields.Selection([('block', 'Block'), ('open', 'Open')], default='open', string="Block Pengiriman")
    x_kebutuhan_pengiriman_ids = fields.Many2many('x.kebutuhan.pengiriman', string="Kebutuhan Pengiriman")
    is_berikat = fields.Char('berikat')

    # Cek apakah user login adalah marketing
    @api.one
    def is_mkt_act(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user:
            id = res_user.id
            # Jika yg login pak fahrur atau ikawati
            if id == 20 or id == 124:
                self.is_mkt = False

            elif res_user.has_group('sales_team.group_sale_salesman') or \
                    res_user.has_group('sales_team.group_sale_salesman_all_leads') or \
                    id == 8:
                self.is_mkt = True

            else:
                self.is_mkt = False

    # Cek apakah user login adalah administrator
    @api.one
    def is_admin_act(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('base.group_system'):
            self.is_administrator = True
        else:
            self.is_administrator = False


    # Function for update x_block_customer untuk SO
    @api.multi
    def write(self, vals):
        res = super(res_partner, self).write(vals)

        for partner in self:
            partner_name = partner.name
            sale_order = self.env['sale.order'].search(
                [('state', 'in', ['draft', 'sent']), ('partner_id', '=', partner_name)])
            if sale_order:
                for sale_order_new in sale_order:
                    block_customer = partner.x_block_customer
                    if block_customer == 'no':
                        sale_order_new.update({'is_block': 'no'})
                    if block_customer == 'yes':
                        sale_order_new.update({'is_block': 'yes'})
                return res

            else:
                return res

class KebutuhanPengiriman(models.Model):
    _name = 'x.kebutuhan.pengiriman'

    name = fields.Char('Kebutuhan Pengiriman')