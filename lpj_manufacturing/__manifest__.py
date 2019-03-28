
# -*- coding: utf-8 -*-
{
    'name': "lpj_manufacturing",

    'summary': """
        Checkin """,

    'description': """
       Modul untuk inherit Manufacturing Order
       1. routing.py untuk tambahkan default duration routing in second
       2. minmax.py untuk tambahkan fields minmax di MO parent
       3. penambahan cetak lot barang ada di minmax
       4. penambahan cetak lot sj ada di sj_lot
    """,

    'author': "IT03",
    'website': "",
    
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale', 'mrp', 'lpj_cusrequire', 'report'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        # 'views/sales.xml',
        'views/routing.xml',
        'views/minmax.xml',
        'views/config_waste.xml',
        'views/meter_to_pcs.xml',
        'views/mrp_production.xml',
        'views/refresh_bom.xml',
        'views/sale_order.xml',
        'views/popup_message.xml',
        'views/workorder.xml',
        'views/report.xml',
        'views/report_bom.xml',
        'views/report_ok_non_sticker.xml',
        'views/menu.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
