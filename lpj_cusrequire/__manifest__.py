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
    'depends': ['base', 'product', 'mrp', 'lpj_product', 'mail', 'sale', 'crm', 'sale_crm'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'security/security_pde.xml',
        'views/approval_product.xml',
        'views/quotation_cr.xml',
        'views/sq.xml',
        'views/report_sph.xml',
        'views/mail_template_sph.xml',
        'views/sph_report_template.xml',
        'views/history_duedate.xml',
        # 'views/admin_input_product.xml',
        'views/sale_view.xml',
        'views/crm.xml',
        'views/print_quo.xml',
        'views/report_quotation.xml',
        'views/config_bahan.xml',
        'views/config_feature.xml',
        'views/config_diecut.xml',
        'views/config_tinta.xml',
        'views/config_mesin.xml',
        'views/config_product_type.xml',
        'views/config_process_cost.xml',
        'views/config_plate_cost.xml',
        'views/config_waste_table.xml',
        'views/config_profit_margin.xml',
        'views/history_precosting.xml',
        'views/report_quotation_ppn.xml',
        'views/config_qty_roundup.xml',
        'views/approval_gm.xml',
        'views/sale_report_inherit.xml',
        'views/config_kategori.xml',
        'views/precost_price_range.xml',
        'views/menu.xml',
        'views/purchase_req.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
