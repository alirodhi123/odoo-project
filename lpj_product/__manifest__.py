# -*- coding: utf-8 -*-
{
    'name': "lpj_product",

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
    'depends': ['product', 'sale', 'mrp', 'quality_assurance', 'purchase', 'base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'security/security.xml',
        'views/diecut_shape.xml',
        'views/category_finishing_product.xml',
        'views/category_finishing_process.xml',
        'views/master_color.xml',
        'views/ink_coverage.xml',
        'views/hotprint_list.xml',
        'views/varnish_list.xml',
        'views/packing_roll.xml',
        'views/layout_product.xml',
        'views/property_product.xml',
        'views/quality_assurance.xml',
        'views/precosting_manufac.xml',
        'views/drawing.xml',
        'views/tds.xml',
        'views/menu.xml',
        'views/sequences.xml',
        'views/product_view_standard_price.xml',
        # 'views/report_label_plate.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
