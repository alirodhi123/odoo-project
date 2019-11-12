# -*- coding: utf-8 -*-
{
    'name': "Employee's Training Management",



    'author': "Mahmoud Elsaka",
    'website': "http://www.elsaka.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Employees',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','mail','hr'],

    # always loaded
    'data': [

        'security/training_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/sequence.xml',
        'views/training_employee.xml',
        'views/training_tags.xml',
        # 'views/course_schedule_inherit.xml',
        'views/menu.xml'
    ],
    
       'images': ['static/description/icon-web.png'],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
