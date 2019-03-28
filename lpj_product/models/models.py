# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class data_form(models.Model):
    _inherit = 'product.template'
    _name = 'product.template'

    x_pp_template = fields.One2many('product.product','product_tmpl_id',string='roduct_product')
    x_is_trial = fields.Boolean(string = 'is trial', default=True)
    x_pic_trial = fields.Char(default = 'BARANG TRIAL')
    x_internal = fields.Char(related = 'categ_id.name')
    # x_status_input = fields.Selection([('none', 'None'),('inputbarang', 'Input Product'),('validatorproduct', 'Validator Input Product')
    #                                       , ('inputbomtinta', 'Input BOM Tinta'),('validatortinta', 'Validator Tinta')
    #                                       , ('9', 'Input BOM Plate'),('10', 'Done')],default='none', track_visibility='onchange', string="Status Input")
    x_status_admin_input = fields.Selection([('1', 'Input Product'),('2', 'Validator Input Product')
                                          , ('3', 'Input BOM Tinta'),('4', 'Validator Tinta')
                                          , ('5', 'Input BOM Plate'),('6', 'Done')],default='1', track_visibility='onchange', string="Status Input")
    x_input_deskripsi = fields.Text(string="Keterangan untuk input data")
    x_user_input = fields.Many2one('res.partner', string='User Input',
                                   domain=[('customer', '=', False), ('supplier', '=', False)])
    x_user_validator = fields.Many2one('res.partner', string='User Validator',
                                       domain=[('customer', '=', False), ('supplier', '=', False)])

    # DataForm
    x_ink_coverage_pde = fields.One2many('x.ink.coverage', 'x_product_id', 'Ink Coverage', track_visibility='onchange')
    x_finishing_product_ids = fields.One2many('x.category.finishing.product', 'x_product_id', 'Finishing Product',
                                              track_visibility='onchange')
    x_hotprint_list_ids = fields.One2many('x.hotprint.list', 'x_product_id', 'Hotprint', track_visibility='onchange')
    x_finishing_process_laminating = fields.Many2one('x.category.finishing.process', 'Laminating',
                                                     domain=[('x_is_laminating', '=', True)],
                                                     track_visibility='onchange')
    x_finishing_process_emboss = fields.Many2one('x.category.finishing.process', 'Emboss',
                                                 domain=[('x_is_emboss', '=', True)], track_visibility='onchange')
    x_varnish_list_ids = fields.One2many('x.varnish.list', 'x_product_id', 'Varnish', track_visibility='onchange')
    x_finishing_process_foil = fields.Many2one('x.category.finishing.process', 'Category Foil',
                                               domain=[('x_is_foil', '=', True)], track_visibility='onchange')
    x_layout_product_ids = fields.One2many('x.layout.product', 'x_product_id', 'Layout Product',
                                           track_visibility='onchange')
    x_layout_plong_ids = fields.One2many('x.layout.plong', 'x_plongproduct_id', 'Layout Second Pass',
                                           track_visibility='onchange')
    x_media_tempel = fields.Char("Media Tempel", track_visibility='onchange')
    x_location_media_id = fields.One2many('x.location.media.sticker', 'x_product_id', 'Media Location',
                                          track_visibility='onchange')
    x_gramature_product = fields.Float(string="Gramature (gsm)", track_visibility='onchange')
    x_thickness_product = fields.Float(string="Thickness (mikron)", track_visibility='onchange')
    x_keterangan_lem = fields.Text(string="Keterangan Lem", track_visibility='onchange')
    x_material_type_coa = fields.Char(string="Material Type")
    x_length = fields.Float('Length (mm)')
    x_width_variant = fields.Char(string = 'Variant', readonly = True, compute = '_get_variant')
    x_width = fields.Float('Width (mm)', track_visibility='onchange')
    x_length_m = fields.Float(readonly=True, store=True, compute="check_konversi",
                              digits=dp.get_precision('Payment Terms'))
    x_width_m = fields.Float(readonly=True, store=True, compute="check_konversi",
                             digits=dp.get_precision('Payment Terms'))
    x_special_color = fields.Boolean('Special Color', track_visibility='onchange')
    x_diecut_shape_id = fields.Many2one('x.diecut.shape', 'Diecut Shape', track_visibility='onchange')
    x_material_type_ids = fields.One2many('x.material.type', 'x_product_id', 'Material Type',
                                              track_visibility='onchange')
    x_release = fields.Many2one('x.release', 'Release', track_visibility='onchange')

    x_type_packing = fields.Selection([('roll','Roll'),('sheet','Sheet'),('fanfold ','Fan Fold')], track_visibility='onchange',string='Type Packing')
    x_pcs_units = fields.Float(string='Pcs per Roll/Sheet/Fold', track_visibility='onchange')
    x_units_packing = fields.Float(string='Roll/Sheet per Packing', track_visibility='onchange')
    x_packing_box = fields.Float(string='Pack/Fold per Box', track_visibility='onchange')
    x_inner_core = fields.Char('Inner Core Diameter (mm)', track_visibility='onchange')
    x_thicknes_core = fields.Char('Thicknes Core (mm)', track_visibility='onchange')
    x_outer_core = fields.Char('Outer Core Diameter (mm)', track_visibility='onchange')
    x_roll_direction = fields.Many2one('x.packing.roll.direction', 'Roll Direction', track_visibility='onchange')
    x_roll_file = fields.Binary(related='x_roll_direction.x_image')
    x_hasil_bungkus = fields.Many2one('x.hasil.bungkus', 'Hasil Bungkus', track_visibility='onchange')
    x_jarak_druk = fields.Float('Jarak Druk(mm)', track_visibility='onchange')
    x_jarak_druk_m = fields.Float(readonly=True, store=True, compute="check_konversi",
                                  digits=dp.get_precision('Payment Terms'))
    x_lebar_bahan = fields.Float('Lebar Bahan(mm)', track_visibility='onchange')
    x_lebar_bahan_m = fields.Float(readonly=True, store=True, compute="check_konversi",
                                   digits=dp.get_precision('Payment Terms'))
    x_isi_druk = fields.Float('Isi Druk(pcs)', track_visibility='onchange')
    x_drawing = fields.Many2one('x.drawing', 'Drawing')
    x_drawing_file = fields.Binary(related='x_drawing.x_file')
    x_tds = fields.Many2one('x.tds', 'TDS')
    x_customer = fields.Many2one('res.partner', string='Customer/Suppler', domain=['|',('customer', '=', True),('supplier', '=', True)])
    # x_product_product = fields.Many2many('product_product','product_tmpl_id', string = 'product_product_template')
    # ribbon spech
    x_ribbon = fields.Many2one('x.ribbon.type', 'Ribbon Type')
    x_face_ink = fields.Selection([('in', 'IN'), ('out', 'OUT')], string='Face Ink')
    x_id_core = fields.Float('ID Core(mm)')
    x_id_core_m = fields.Float('ID Core')
    x_od_core = fields.Float('OD Core(mm)')
    x_od_core_m = fields.Float('OD Core')
    x_core_type = fields.Selection([('single', 'Single'), ('double', 'Double')], string='Core Type')
    x_notch = fields.Boolean('With Notch')
    x_roll_perbox_ribbon = fields.Integer('Roll Perbox')
    x_material_core = fields.Selection([('paper', 'Paper'), ('plastic', 'Plastic')], string='Material Core')
    # Code
    x_code = fields.Char("My Code")


    @api.depends("x_length", "x_width", "x_jarak_druk", "x_lebar_bahan", "categ_id", "x_id_core", "x_od_core")
    def check_konversi(self):
        if self.x_length > 0:
            self.x_length_m = self.x_length / 1000
        if self.x_width > 0:
            self.x_width_m = self.x_width / 1000
        if self.x_jarak_druk > 0:
            self.x_jarak_druk_m = self.x_jarak_druk / 1000
        if self.x_lebar_bahan > 0:
            self.x_lebar_bahan_m = self.x_lebar_bahan / 1000
        if self.x_id_core > 0:
            self.x_id_core_m = self.x_id_core / 1000
        if self.x_od_core > 0:
            self.x_od_core_m = self.x_od_core / 1000


    @api.one
    def _get_variant(self):
        self.x_width_variant = self.id
        self.env.cr.execute("select pav.name from product_attribute_value_product_product_rel ppr "
                            "left join product_attribute_value pav on ppr.product_attribute_value_id = pav.id "
                            "left join product_attribute pa on pav.attribute_id = pa.id "
                            "left join product_product pp on ppr.product_product_id = pp.id "
                            "left join product_template pt on pp.product_tmpl_id = pt.id "
                            "where pa.name = 'Lebaran' and pp.barcode = '" + str(self.barcode) + "'")
        # self.x_width_variant = self.env.cr.fetchone()[0]


class hasil_bungkus(models.Model):
    _name = 'x.hasil.bungkus'

    name = fields.Char(required=True)
    description = fields.Text(string='Description')

class pp_variant(models.Model):
    _inherit = 'product.product'

    x_variant_value  = fields.Char(readonly=True, compute = '_pp_variant')
    x_qty_mpersegi = fields.Float(string = 'Quantity Meter Persegi', compute = '_perkalian')


    @api.one
    def _pp_variant(self):
        if self.barcode:
            self.env.cr.execute("select pav.name from product_attribute_value_product_product_rel ppr "
                                "left join product_attribute_value pav on ppr.product_attribute_value_id = pav.id "
                                "left join product_attribute pa on pav.attribute_id = pa.id "
                                "left join product_product pp on ppr.product_product_id = pp.id "
                                "left join product_template pt on pp.product_tmpl_id = pt.id "
                                "where pa.name = 'Lebaran' and pp.barcode = '" + self.barcode + "'")
            a = self.env.cr.fetchone()
            if a:
                self.x_variant_value = a[0]
                self.x_variant_value = (float(self.x_variant_value)/1000)
                return self.x_variant_value
            else:
                return None

    @api.one
    def _perkalian(self):
        self.x_qty_mpersegi = int(self.qty_available) * float(self.x_variant_value)



class diecut_shape(models.Model):
    _name = 'x.diecut.shape'

    name = fields.Char(required=True)
    description = fields.Text(string='Description')


class diecut_type(models.Model):
    _name = 'x.diecut.type'

    name = fields.Char(required=True)
    description = fields.Text(string='Diecut Type')


class plate_type(models.Model):
    _name = 'x.plate.type'

    name = fields.Char(required=True)
    description = fields.Text(string='Plate Type')


class category_finishing_product(models.Model):
    _name = 'x.category.finishing.product'

    name = fields.Char(required=True)
    description = fields.Text(string='Description')
    x_product_id = fields.Many2one('product.template', string='Product Id')


class category_finishing_process(models.Model):
    _name = 'x.category.finishing.process'

    name = fields.Char(required=True)
    x_is_laminating = fields.Boolean('Is Laminating Category')
    x_is_hotprint = fields.Boolean('Is Hotprint Category')
    x_is_emboss = fields.Boolean('Is Emboss Category')
    x_is_varnish = fields.Boolean('Is Varnish Category')
    x_is_foil = fields.Boolean('Is Foil Category')
    description = fields.Text(string='Description')


class master_colour(models.Model):
    _name = 'x.master.color'

    name = fields.Char(required=True)
    description = fields.Text(string='Description')
    x_parent_id = fields.Many2one('x.master.color', Index=True, Store=True, Copy=True)
    x_child_id = fields.One2many('x.master.detail.color', 'x_master_color_ids')
    # x_child_id = fields.One2many('x.master.color','x_parent_id','Color',Store=True)
    x_is_campuran = fields.Boolean(string='Mix Colors')
    # precentage = fields.Float('precentage(%)')


class master_colour_detail(models.Model):
    _name = 'x.master.detail.color'

    precentage = fields.Float('precentage(%)')
    x_master_color_ids = fields.Many2one('x.master.color', string='Color', Store=True)
    # x_master_color_ids = fields.Char()
    description = fields.Text(string='Description')


class category_printing(models.Model):
    _name = 'x.category.printing'

    name = fields.Char(required=True)
    description = fields.Text(string='Description')


class material_type(models.Model):
    _name = 'x.material.type'

    name = fields.Many2one('product.template', 'Material Type')
    x_is_main = fields.Boolean('Is Main')
    description = fields.Text(string='Description')
    x_product_id = fields.Many2one('product.template', string='Product Id')


class packing_category(models.Model):
    _name = 'x.packing.category'

    name = fields.Char(required=True)
    description = fields.Text(string='Description')
    # x_product_id = fields.Many2one('product.template',string='Product Id')


class release(models.Model):
    _name = 'x.release'

    name = fields.Char(required=True)
    description = fields.Text(string='Description')

#
class ink_coverage(models.Model):
    _name = 'x.ink.coverage'

    description = fields.Text(string='Description')
    x_category_printing_id = fields.Many2one('x.category.printing', string='Category Printing')
    x_colors_id = fields.Many2one('x.master.color', string='Color')
    x_coverage = fields.Selection([('0.0', '0.0'), ('0.25', '0.25'), ('0.5', '0.5'), ('0.75', '0.75'), ('1', '1')],
                                  string='Coverage')
    x_product_id = fields.Many2one('product.template', string='Product Id')


class hot_print_list(models.Model):
    _name = 'x.hotprint.list'

    description = fields.Text(string='Description')
    x_category_finishing_process_id = fields.Many2one('x.category.finishing.process',
                                                      string='Finishing Process Hotprint',
                                                      domain=[('x_is_hotprint', '=', True)])
    x_product_id = fields.Many2one('product.template', string='Product Id')


class varnish_list(models.Model):
    _name = 'x.varnish.list'

    description = fields.Text(string='Description')
    x_category_finishing_process_id = fields.Many2one('x.category.finishing.process',
                                                      string='Finishing Process Varnish',
                                                      domain=[('x_is_varnish', '=', True)])
    x_product_id = fields.Many2one('product.template', string='Product Id')


class packing_roll_direction(models.Model):
    _name = 'x.packing.roll.direction'

    name = fields.Char(required=True)
    description = fields.Text(string='Description')
    x_image = fields.Binary('Image')
    # x_product_id = fields.Many2one('product.template',string='Product Id')


class layout_product(models.Model):
    _name = 'x.layout.product'

    x_type = fields.Selection([('across', 'Across'), ('arround', 'Arround')], string='Type')
    x_size = fields.Float('Ukuran (mm)')
    x_druk = fields.Float('Jarak Druk (mm)', compute='_calcdruk')
    x_space = fields.Float('Space (mm)')
    x_number = fields.Integer('Number')
    x_std_afalan = fields.Float('Std Afalan (mm)')
    x_jumlah = fields.Float('Ref. Lebaran Bahan (mm)', compute='_calclebaran')
    x_product_id = fields.Many2one('product.template', string='Product Id')

    @api.one
    @api.depends("x_size","x_space")
    def _calcdruk(self):
        self.x_druk = self.x_size + self.x_space

    @api.one
    @api.depends("x_druk", "x_number","x_std_afalan")
    def _calclebaran(self):
        self.x_jumlah = (self.x_druk * self.x_number) + self.x_std_afalan

class layout_plong(models.Model):
    _name = 'x.layout.plong'

    x_plong_type = fields.Selection([('across', 'Across'), ('arround', 'Arround')], string='Type')
    x_plong_size = fields.Float('Ukuran (mm)')
    x_plong_druk = fields.Float('Jarak Druk (mm)', compute='_hitungdruk')
    x_plong_space = fields.Float('Space (mm)')
    x_plong_number = fields.Integer('Number')
    x_plongstd_afalan = fields.Float('Std Afalan (mm)')
    x_plong_jumlah = fields.Float('Ref. Lebaran Bahan (mm)', compute='_hitunglebaran')
    x_plongproduct_id = fields.Many2one('product.template', string='Product Id')

    @api.one
    @api.depends("x_plong_size","x_plong_space")
    def _hitungdruk(self):
        self.x_plong_druk = self.x_plong_size + self.x_plong_space

    @api.one
    @api.depends("x_plong_druk", "x_plong_number","x_plongstd_afalan")
    def _hitunglebaran(self):
        self.x_plong_jumlah = (self.x_plong_druk * self.x_plong_number) + self.x_plongstd_afalan

class location_media(models.Model):
    _name = 'x.location.media.sticker'

    name = fields.Char(required=True)
    description = fields.Text(string='Description')
    x_product_id = fields.Many2one('product.template', string='Product Id')


class ribbon_type(models.Model):
    _name = 'x.ribbon.type'

    name = fields.Char(required=True)
    description = fields.Text(string='Plate Type')

class ribbon_type(models.Model):
    _name = 'x.ribbon.type'

    name = fields.Char(required=True)
    description = fields.Text(string='Plate Type')





