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
    'depends': ['base', 'account', 'sale', 'report', 'lpj_cusrequire', 'stock', 'purchase', 'report_xlsx'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/sequences.xml',
        # 'views/down_payment.xml',
        # 'report/report_kuitansi.xml',
        'views/report_kuitansi.xml',
        'views/report_invoice.xml',
        'views/report_vendor_bill.xml',
        'views/report_nota.xml',
        'views/report_invoice_include.xml',
        'views/report_payment.xml',
        'views/report_kuitansi_include.xml',
        'views/report_invoice_include_new.xml',
        'views/invoice.xml',
        'views/stock_picking.xml',
        'views/due_date_pembayaran.xml',
        'views/account_payment.xml',
        'views/general_ledger_inherit.xml',
        'views/balance_sheet_inherit.xml',
        'demo/demo.xml',
        'views/menu.xml',
        'report/report_general_ledger_xlsx.xml',
        'report/report_balance_sheet_xlsx.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}