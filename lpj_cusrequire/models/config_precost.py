from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp
from datetime import datetime
from dateutil.relativedelta import relativedelta


class ConfigBahan(models.Model):
    _name = 'x.config.bahan'

    name = fields.Char('Nama Bahan', compute='cek_name', store=True)
    x_bahan = fields.Many2one('product.template', 'Material Type',
                           domain=[('categ_id.sts_bhn_utama.name', '=', 'Bahan Utama')])
    x_kategori_1 = fields.Float(string='Kategori I (200-999)m2')
    x_kategori_2 = fields.Float(string='Kategori II (1000-2499)m2')
    x_kategori_3 = fields.Float(string='Kategori III (>2500)m2')

    x_kategori = fields.One2many('x.harga.kategori.bahan', 'x_bahan_id', string='Harga Kategori')

    @api.depends("x_bahan")
    def cek_name(self):
        if self.x_bahan:
            self.env.cr.execute(
                        "select name from product_template where id = "+ str(self.x_bahan.id))
            sql = self.env.cr.fetchone()
            self.name = sql[0]

#
# class ConfigFinishing(models.Model):
#     _name = 'x.config.finishing'
#
#     name = fields.Char('Jenis Finishing')
#     x_harga_m2 = fields.Float(string = 'Harga m2')

# class ConfigDiecut(models.Model):
#     _name = 'x.config.diecut'
#
#     name = fields.Many2one('product.template', 'PL&DC',
#                                          domain=[('categ_id.sts_bhn_utama.name', '=', 'PL&DC')])
#     x_harga_m2 = fields.Float(string = 'Harga m2')

class ConfigTinta(models.Model):
    _name = 'x.config.tinta'
    name = fields.Char('Number of Color')
    x_kategori_1 = fields.Float(string='Kategori I (200-999)m2')
    x_kategori_2 = fields.Float(string='Kategori II (1000-2499)m2')
    x_kategori_3 = fields.Float(string='Kategori III (>2500)m2')
    x_kategori = fields.One2many('x.harga.kategori.tinta', 'x_tinta_id', string='Harga Kategori')

class ConfigMesin(models.Model):
    _name = 'x.config.mesin'

    name = fields.Char('Jenis Mesin')
    x_harga_m2 = fields.Float(string = 'Harga m2')

# ---------------------------------------------------------------------------------------
class ProductType(models.Model):
    _name = 'x.product.type.precost'

    # name =  fields.Selection([('stc_label', 'Sticker Label'), ('inmold', 'In-Mold Label'), ('shrink', 'Shrink Label'),
    #                           ('carton', 'Carton Packaging'), ('flexible', 'Flexible Packaging'), ('blank_shrink', 'Blank Shrink Label'),
    #                           ('blank_stc', 'Blank Sticker Label')],
    #                                         default='stc_label', string='Product Type',
    #                                         track_visibility='onchange', required=True)
    name = fields.Char(string = 'Product Type')
    x_moq = fields.Float(string = 'MOQ m2')
    x_ids_proces_cost = fields.Many2many('x.process.cost.precost', string="Process Cost")


class ProcessCost(models.Model):
    _name = 'x.process.cost.precost'

    name = fields.Char('Process List')
    x_kategori_1 = fields.Float(string = 'Kategori I (200-999)m2')
    x_kategori_2 = fields.Float(string='Kategori II (1000-2499)m2')
    x_kategori_3 = fields.Float(string='Kategori III (>2500)m2')
    x_kategori = fields.One2many('x.harga.kategori.proses', 'x_proses_id', string='Harga Kategori')

# class InkCost(models.Model):
#     _name = 'x.ink.cost.precost'
#
#     name = fields.Char('Number of Color')
#     x_kategori_1 = fields.Float(string = 'Kategori I (200-999)m2')
#     x_kategori_2 = fields.Float(string='Kategori II (1000-2499)m2')
#     x_kategori_3 = fields.Float(string='Kategori III (>2500)m2')

class FeatureCost(models.Model):
    _name = 'x.feature.cost.precost'

    name = fields.Char('Feature List')
    x_kategori_1 = fields.Float(string = 'Kategori I (200-999)m2')
    x_kategori_2 = fields.Float(string='Kategori II (1000-2499)m2')
    x_kategori_3 = fields.Float(string='Kategori III (>2500)m2')
    x_kategori = fields.One2many('x.harga.kategori.feature', 'x_feature_id', string='Harga Kategori')

class PlateCost(models.Model):
    _name = 'x.plate.cost.precost'

    name = fields.Char('Number of Plate')
    x_kategori_1 = fields.Float(string = 'Kategori I (200-999)m2')
    x_kategori_2 = fields.Float(string='Kategori II (1000-2499)m2')
    x_kategori_3 = fields.Float(string='Kategori III (>2500)m2')
    x_kategori = fields.One2many('x.harga.kategori.plate', 'x_plate_id', string='Harga Kategori')

class DiecutCost(models.Model):
    _name = 'x.diecut.cost.precost'

    # name = fields.Many2one('x.product.type.precost')
    name = fields.Many2one('x.product.type.precost', string='Product Type')
    x_kategori_1 = fields.Float(string = 'Kategori I (200-999)m2')
    x_kategori_2 = fields.Float(string='Kategori II (1000-2499)m2')
    x_kategori_3 = fields.Float(string='Kategori III (>2500)m2')
    x_kategori = fields.One2many('x.harga.kategori.diecut', 'x_diecut_id', string='Harga Kategori')


class WasteTable(models.Model):
    _name = 'x.waste.table.precost'

    # name = fields.Many2one('x.product.type.precost')
    name = fields.Char('Product Area m2')
    x_batas_atas = fields.Float(store=True,digits=(16,5), string='Batas Atas m2/pcs')
    x_batas_bawah = fields.Float(store=True,digits=(16,5), string='Batas Bawah m2/pcs')
    x_waste_config = fields.Char('Waste Config %')
    x_kategori_1 = fields.Float(string = 'Kategori I (200-999)m2')
    x_kategori_2 = fields.Float(string='Kategori II (1000-2499)m2')
    x_kategori_3 = fields.Float(string='Kategori III (>2500)m2')
    x_kategori = fields.One2many('x.harga.kategori.waste', 'x_waste_id', string='Harga Kategori')

class ProfitMargin(models.Model):
    _name = 'x.profit.margin.precost'

    # name = fields.Many2one('x.product.type.precost')
    name = fields.Char('PM List')
    x_percentage = fields.Float(string = 'Percentage')


class HistoryPrecosting(models.Model):
    _name = 'x.history.precosting'

    # name = fields.Many2one('x.product.type.precost')
    name = fields.Char('SQ')
    x_id_sq = fields.Many2one('x.sales.quotation', string= 'No SQ')
    x_length = fields.Float(string = 'Length (mm)')
    x_width = fields.Float(string = 'Width (mm)')
    x_length_m = fields.Float(string='Length (m)')
    x_width_m = fields.Float(string='Width (m)')
    x_quantity = fields.Float(string = 'Quantity')
    x_area_m2_pcs = fields.Float(string = 'm2/pcs')
    x_area_m2_tot = fields.Float(string = 'm2')
    x_waste_produksi = fields.Float(string = 'Waste Produksi (%)')
    x_waste_config = fields.Float(string = 'Waste Config (%)')
    x_total_waste_m2 = fields.Float(string = 'Total Waste m2')
    x_category = fields.Integer(string = 'Category')

class qty_roundup(models.Model):
    _name = 'x.qty.roundup'
    name = fields.Char(String='Qty Roundup')

class ConfigKategori(models.Model):
    _name = 'x.config.kategori.precost'

    # name = fields.Many2one('x.product.type.precost')
    name = fields.Char('Kategori')
    x_nomor = fields.Integer('Nomor', compute='check_konversi', store=True)
    x_batas_atas = fields.Float(store=True,digits=(16,2), string='Batas Atas (m2)')
    x_batas_bawah = fields.Float(store=True,digits=(16,2), string='Batas Bawah (m2)')
    x_config_bahan = fields.One2many('x.harga.kategori.bahan', 'x_kategori_id')
    x_config_tinta = fields.One2many('x.harga.kategori.tinta', 'x_kategori_id')
    x_config_proses = fields.One2many('x.harga.kategori.proses', 'x_kategori_id')
    x_config_feature = fields.One2many('x.harga.kategori.feature', 'x_kategori_id')
    x_config_plate = fields.One2many('x.harga.kategori.plate', 'x_kategori_id')
    x_config_diecut = fields.One2many('x.harga.kategori.diecut', 'x_kategori_id')
    x_config_wasate = fields.One2many('x.harga.kategori.waste', 'x_kategori_id')



    @api.depends("name")
    def check_konversi(self):
        if self.name:
            [
                int(s) for s in self.name.split()
                if s.isdigit()
            ]
            self.x_nomor = s

class ConfigHargaBahan(models.Model):
    _name = 'x.harga.kategori.bahan'

    # name = fields.Float(string = 'Name', related='x_harga', store=True)
    x_bahan_id = fields.Many2one('x.config.bahan', string='Nama Bahan')
    x_kategori_id = fields.Many2one('x.config.kategori.precost', string='Kategori')
    x_harga = fields.Float(string = 'Harga')

class ConfigHargaTinta(models.Model):
    _name = 'x.harga.kategori.tinta'

    # name = fields.Many2one('x.product.type.precost')
    x_tinta_id = fields.Many2one('x.config.tinta', string='Nama Tinta')
    x_kategori_id = fields.Many2one('x.config.kategori.precost', string='Kategori')
    x_harga = fields.Float(string = 'Harga')

class ConfigHargaProses(models.Model):
    _name = 'x.harga.kategori.proses'

    # name = fields.Many2one('x.product.type.precost')
    x_proses_id = fields.Many2one('x.process.cost.precost', string='Nama Proses')
    x_kategori_id = fields.Many2one('x.config.kategori.precost', string='Kategori')
    x_harga = fields.Float(string = 'Harga')

class ConfigHargaFeature(models.Model):
    _name = 'x.harga.kategori.feature'

    # @api.model
    # def _default_feature_id(self):
    #     if self._context.get('active_model') == 'x.feature.cost.precost':
    #         return self._context.get('active_id')
    #     else:
    #         id = self._context.get('parent_id')
    #         return id
    #     return False

    x_feature_id = fields.Many2one('x.feature.cost.precost', string='Nama Feature')
    x_kategori_id = fields.Many2one('x.config.kategori.precost', string='Kategori')
    x_harga = fields.Float(string = 'Harga')



class ConfigHargaPlate(models.Model):
    _name = 'x.harga.kategori.plate'

    # name = fields.Many2one('x.product.type.precost')
    x_plate_id = fields.Many2one('x.plate.cost.precost', string='Nama Plate')
    x_kategori_id = fields.Many2one('x.config.kategori.precost', string='Kategori')
    x_harga = fields.Float(string = 'Harga')


class ConfigHargaDiecut(models.Model):
    _name = 'x.harga.kategori.diecut'

    # name = fields.Many2one('x.product.type.precost')
    x_diecut_id = fields.Many2one('x.diecut.cost.precost', string='Nama Diecut')
    x_kategori_id = fields.Many2one('x.config.kategori.precost', string='Kategori')
    x_harga = fields.Float(string = 'Harga')


class ConfigHargaWaste(models.Model):
    _name = 'x.harga.kategori.waste'

    # name = fields.Many2one('x.product.type.precost')
    x_waste_id = fields.Many2one('x.waste.table.precost', string='Nama Waste')
    x_kategori_id = fields.Many2one('x.config.kategori.precost', string='Kategori')
    x_harga = fields.Float(string = 'Harga')
