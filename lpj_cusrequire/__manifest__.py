# -*- coding: utf-8 -*-
{
    'name': "lpj_cusrequire",

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
    'depends': ['base', 'product', 'mrp', 'lpj_product', 'mail', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'security/security_pde.xml',
        'views/approval_product.xml',
        'views/quotation_cr.xml',
        # 'views/admin_input_product.xml',
        'views/sale_view.xml',
        'views/print_quo.xml',
        'views/report_quotation.xml',
        'views/menu.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
