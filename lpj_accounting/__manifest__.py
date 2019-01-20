# -*- coding: utf-8 -*-
{
    'name': "lpj_accounting",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'sale', 'report', 'lpj_cusrequire', 'stock', 'purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/sequences.xml',
        # 'views/down_payment.xml',
        # 'report/report_kuitansi.xml',
        'views/report_kuitansi.xml',
        'views/report_invoice.xml',
        'views/invoice.xml',
        'views/stock_picking.xml',
        'views/due_date_pembayaran.xml',
        'demo/demo.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}