
# -*- coding: utf-8 -*-
{
    'name': "Training Odoo",

    'summary': """
        Modul untuk latihan tehcnical """,

    'description': """
        Modul ini berfungsi untuk menjalankan technical documentation pada website resmi odoo.com. Bahan yang dipelajari adalah :\n
        - ORM\n
        - Berbagai View\n
        - Report\n
        - Wizard\n
        - Dll
    """,

    'author': "Muhammad Aziz",
    'website': "http://www.tutorialopenerp.wordpress.com",
    
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/partner.xml',
        'wizard/wizard_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
