
# -*- coding: utf-8 -*-
{
    'name': "lpj_contact",

    'summary': """
        Checkin """,

    'description': """
       Modul untuk inherit contact
    """,

    'author': "ITE LPJ",
    'website': "laprintjaya.com",
    
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        # 'views/sales.xml',
        'views/rtrw.xml',
        'views/res_partner.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
