# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class stock_picking(models.Model):
    _inherit = 'stock.picking'

    coa_ids = fields.Many2one('x.coa')
    product_name_id = fields.Char(related='pack_operation_product_ids.product_name')
    product_id_new = fields.Char(related='pack_operation_product_ids.product_id.name')
    x_partner_id = fields.Char(related="partner_id.name")


class stock_pickingi_ids(models.Model):
    _inherit = 'stock.pack.operation'


    product_temp = fields.Many2one('product.template')
    product_name = fields.Char(string="Product Ali", compute='_get_product_name')

    # Get semua nama product pada model stock.pack.operation
    @api.one
    @api.depends('product_id', 'product_id.name')
    def _get_product_name(self):
        product_temp = self.product_id.name
        self.ensure_one()
        # self.product_name = self.product_id.name
        for x in self:
            if (product_temp > 1) :
                product_temp_new = x.product_id.name
            else:
                product_temp_new = x.product_id.name
        self.product_name = product_temp_new


    # Fungsi parsing data to other view
    @api.multi
    def open_second_class(self):
        ac = self.env['ir.model.data'].xmlid_to_res_id('quality_assurance.coa_form_view', raise_if_not_found=True)
        stock_picking = False
        product = False
        for o in self:
            stock = o.id
            stock_picking = o.picking_id.id
            code_po_cus = o.picking_id.sale_id.x_po_cust
            code_sjk = o.picking_id.x_sj_supplier
            tgl_pemeriksaan = o.picking_id.min_date
            tgl_kirim = o.picking_id.min_date
            product = o.product_id.name
            partner = o.picking_id.x_partner_id
            jumlah_done = o.qty_done
            width = o.product_id.x_width
            lenght = o.product_id.x_length
            gramature = o.product_id.x_gramature_product
            thickness = o.product_id.x_thickness_product
            thickness_rbn = o.product_id.x_thickness_product
            shelflife = o.product_id.life_time
            unit_of_measure = o.product_uom_id.name
            keterangan_lem = o.product_id.x_keterangan_lem
            material_type = o.product_id.x_material_type_quality
            ribbon_type = o.product_id.x_ribbon
            colour_rbn = o.product_id.x_colour
            ink_melting = o.product_id.x_ink_melting
            lenght_rbn = o.product_id.x_length
            width_rbn = o.product_id.x_width
            shelflife_rbn = o.product_id.life_time

            # Looping for one2many value
            lot = ""
            for x in o.pack_lot_ids:
                if lot:
                    lot += ", " + x.lot_id.name
                else:
                    lot = x.lot_id.name

            # Looping product untuk mencari category dan material type
            for row_product in o.product_id:
                category_produk = row_product.categ_id.name

            # Looping untuk partner
            nama_partner = ""
            for row in o.picking_id.partner_id:
                parent = row.parent_id
                # Jika parent kosong
                if parent.active == False:
                    nama_partner = row.name
                else:
                    for i in parent:
                        nama_partner = i.name


        result = {
            'name': '2nd class',
            'view_type': 'form',
            'res_model': 'x.coa',
            'view_id': ac,
            'context': {

                'default_x_stock_id': stock_picking,
                'default_x_no_sjk': code_sjk,
                'default_x_tanggal_pemeriksaan': tgl_pemeriksaan,
                'default_x_po_customer': code_po_cus,
                'default_x_tanggal_kirim': tgl_kirim,
                'default_x_nama_barang': product,
                'default_x_customer': nama_partner,
                'default_x_jumlah': jumlah_done,
                'default_x_width': width,
                'default_x_lenght': lenght,
                'default_x_gramature': gramature,
                'default_x_thickness': thickness,
                'default_x_shelflife': shelflife,
                'default_x_uom': unit_of_measure,
                'default_x_keterangan': keterangan_lem,
                'default_x_kode_material': material_type,
                'default_x_category_produk': category_produk,
                'default_x_ink_ribbon_type': ribbon_type.name,
                'default_x_colour_rbn': colour_rbn,
                'default_x_ink_melting': ink_melting,
                'default_x_thickness_rbn': thickness_rbn,
                'default_x_lenght_rbn': lenght_rbn,
                'default_x_width_rbn': width_rbn,
                'default_x_shelflife_rbn': shelflife_rbn,
            },
            'type': 'ir.actions.act_window',
            'view_mode': 'form'
        }
        return result


class coa(models.Model):
    _name = 'x.coa'
    # _inherits = {'stock.picking': 'x_stock_id'}

    def _default_id(self):
        return self.env['stock.picking'].browse(self._context.get('active_id'))

    def _default_pack(self):
        return self.env['stock.pack.operation'].browse(self._context.get('active_id'))

    # x_coa_details_ids = fields.One2many('x.coa.details', 'x_coa_id')
    name = fields.Char(string="No")
    coa_line_ids = fields.One2many('x.coa.line', 'coa_id')
    x_stock_id = fields.Many2one('stock.picking', string="No SJK", readonly=True, default = _default_id)
    stock_id = fields.Many2one('stock.pack.operation', string="Stock IDS", default = _default_pack)
    x_customer = fields.Char(string="Partner", readonly=True)
    x_tanggal_pemeriksaan = fields.Datetime(string="Tanggal Pemeriksaan", readonly=True)
    x_kode_material = fields.Char(string="Kode Material")
    x_po_customer = fields.Char(string="No PO Customer", readonly=True)
    x_jumlah = fields.Integer(string="Jumlah", readonly=True )
    x_no_sjk = fields.Char(string="No SJK", readonly=True)
    x_tanggal_kirim = fields.Datetime(string="Tanggal Kirim", readonly=True)
    x_batch = fields.Char(string="No Batch")
    x_stock_picking_ids = fields.Many2one('stock.pack.operation')
    x_nama_barang = fields.Char(string="Nama Barang", readonly=True)
    x_uom = fields.Char()
    x_lot = fields.Char(string="No Batch")
    x_keterangan = fields.Text(string="Keterangan Lem")
    x_category_produk = fields.Char(string="Category Produk", readonly=True)

    # Notes field
    product_template_id = fields.Many2one('product.template')
    x_gramature = fields.Float(string="Gramature (gsm)")
    x_thickness = fields.Float(string="Thickness (mikron)")
    x_apperance = fields.Selection([('good', 'Good'), ('average', 'Average'), ('bad', 'Bad')],
                                   string="Apperance", default='good', store=True)
    x_colour = fields.Selection([('good', 'Good'), ('average', 'Average'), ('bad', 'Bad')],
                                string="Colour", default='good', store=True)
    x_diecut = fields.Selection([('good', 'Good'), ('average', 'Average'), ('bad', 'Bad')],
                                string="Die Cut", default='good', store=True)
    x_glueing = fields.Selection([('good', 'Good'), ('average', 'Average'), ('bad', 'Bad')],
                                 string="Glueing", default='good', store=True)
    x_lenght = fields.Float(string="Lenght (+/-1 mm)")
    x_width = fields.Float(string="Width (+/-1 mm)")
    x_shelflife = fields.Char(string="Shelf Life (months)")

    # Notes Fields Ribbon
    x_ink_ribbon_type = fields.Char(string="Ribbon Type (Ink)")
    x_colour_rbn = fields.Char(string="Colour")
    x_ink_melting = fields.Char(string="Ink Melting Point")
    x_thickness_rbn = fields.Char(string="Thickness (mikron)")
    x_lenght_rbn = fields.Char(string="Lenght (+/-1 mm)")
    x_width_rbn = fields.Char(string="Width (+/-1 mm)")
    x_shelflife_rbn = fields.Char(string="Shelf Life (months)")
    x_apperance_rbn = fields.Selection([('good', 'Good'), ('average', 'Average'), ('bad', 'Bad')],
                                   string="Apperance", default='good', store=True)

    # Get lot
    @api.model
    def create(self, vals):
        res = super(coa, self).create(vals)

        # Sequence
        sequence = self.env['ir.sequence'].next_by_code('sequence.coa') or ('New')
        res.update({'name': sequence})

        # Parsing lot from stock picking
        id_line = vals['stock_id']

        stock_pack_operation = self.env['stock.pack.operation']
        lot = []

        lotids = stock_pack_operation.search([('id', '=', id_line)])
        if lotids:
            for line in lotids.pack_lot_ids:
                values = {}
                values['lot_id'] = line.lot_id
                values['qty'] = line.qty
                lot.append((0, 0, values))

            res.update({'coa_line_ids': lot})

        return res


class coa_line(models.Model):
    _name = 'x.coa.line'

    coa_id = fields.Many2one('x.coa')
    lot_id = fields.Many2one('stock.production.lot', string="Lot/Serial Number")
    qty = fields.Float(string="Done")






