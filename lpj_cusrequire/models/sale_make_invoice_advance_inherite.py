import time

from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class sale_make_inv_inherite(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    # Fungsi inherite addons
    # Menambahkan fungsi untuk close SO pada button create invoice
    @api.multi
    def closed_so(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', [])) # Line bawaan addons
        id_so = sale_orders.id

        # FUNGSI CUSTOM ALI, UNTUK CLOSE SO
        # Looping sale_order_line
        for data_line in sale_orders.order_line:

            ordered_qty = data_line.product_uom_qty
            delivered_qty = data_line.qty_delivered

            if id_so:
                self.env.cr.execute("select count(sp) "
                                    "from stock_picking sp "
                                    "left join sale_order so on sp.group_id = so.procurement_group_id "
                                    "where so.id = '" + str(id_so) + "' "
                                    "and sp.state not in ('done', 'cancel')")
                sql = self.env.cr.fetchall()
                if sql:
                    for row in sql:
                        count_stock_picking = row[0]
                        # Jika tidak ada outstanding pengiriman
                        if (count_stock_picking == 0) and (ordered_qty - delivered_qty) <= (ordered_qty * 0.1):
                            data_line.update({'x_status_so_line': True})
                        else:
                            data_line.update({'x_status_so_line': False})

        # Query untuk cek apakah so line ada yang false
        self.env.cr.execute("select count(sol.id) "
                            "from sale_order so "
                            "left join sale_order_line sol on so.id = sol.order_id "
                            "where so.id = '" + str(id_so) + "' and " 
                            "so.id in " 
                                "(select order_id from sale_order_line " 
                                "where x_status_so_line = 'f' "
                                "group by order_id)")
        query = self.env.cr.fetchall()
        for o in query:
            count_sol = o[0]

            if count_sol == 0:
                sale_orders.update({'x_status_so': 'close'})
            else:
                sale_orders.update({'x_status_so': 'open'})



    # INHERITE FUNCTION CREATE INVOICE
    @api.multi
    def create_invoices(self):
        # FUNCTION UPDATE CLOSE SO
        self.closed_so()

        res = super(sale_make_inv_inherite, self).create_invoices()
        return res