
# -*- coding: utf-8 -*-
{
    'name': "lpj_inventory",

    'summary': """
        Checkin """,

    'description': """
       Modul untuk inherit inventory modul
    """,

    'author': "IT03",
    'website': "http://www.tutorialopenerp.wordpress.com",
    
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale', 'mrp'],

    # always loaded
    'data': [
        'views/inventory.xml',
        'views/sj_lot.xml',
        'views/lot_workorder.xml',
        'views/stock_scrap.xml',
        'views/inventory_adjustment.xml',
        'views/sequence.xml',
        'views/report_sjk.xml',
        'views/report_internal_transfer.xml',
        'views/stock_report_view_inherite.xml',
        'views/stock_pack_operation_lot_view.xml',
        'views/message_block_pengiriman_view.xml',
        'views/message_create_lot_view.xml',
        'views/report_lot_popup_do.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
