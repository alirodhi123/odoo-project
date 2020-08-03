from odoo import api, fields, models, _
import time
import csv
from odoo.modules import get_module_path
from odoo.exceptions import UserError

class efaktur_product_wizard(models.TransientModel):
    _name = 'vit.efaktur_product'

    @api.multi
    def confirm_button(self):
        """
        export product yang is_efaktur_exported = False
        update setelah export
        :return: 
        """
        cr = self.env.cr

        headers = [
            'OB',
            'KODE_OBJEK',
            'NAMA',
            'HARGA_SATUAN'
        ]

        mpath = get_module_path('vit_efaktur')

        csvfile = open(mpath + '/static/product.csv', 'wb')
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow([h.upper() for h in headers])

        product = self.env['product.template']
        # products = product.search([('is_efaktur_exported','=',False), ('default_code', '=', '5-01-WAX01-229-000-00')])
        products = product.search([('is_efaktur_exported','=',False), ('active', '=', True), ('categ_id', '=', 7), ('sale_ok', '=', True)])
        if products:
            i=0
            for prod in products:
                default_code = str(prod.default_code)
                name = prod.name
                list_price = str(prod.list_price)

                data = {
                    'OB'        : 'OB',
                    'KODE_OBJEK': default_code,
                    'NAMA'      : name.encode('utf-8'),
                    'HARGA_SATUAN': list_price
                }
                csvwriter.writerow([data[v] for v in headers])

                prod.is_efaktur_exported=True
                prod.date_efaktur_exported=time.strftime("%Y-%m-%d %H:%M:%S")
                i+=1

            cr.commit()
            csvfile.close()

            raise UserError("Export %s record(s) Done!" % i)
