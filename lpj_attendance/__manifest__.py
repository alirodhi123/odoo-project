# -*- coding: utf-8 -*-
{
    'name': "lpj_attendance",

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
    'depends': ['base', 'hr_attendance', 'web', 'mrp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/attendance_temp.xml',
        'views/attendance_attendance_view.xml',
        'views/shift_employee_view.xml',
        'views/shift_master_view.xml',
        'views/detail_mesin_shift_view.xml',
        'views/shift_employee_report.xml',
        'wizard/wizard_view.xml',
        'wizard/get_employee_view.xml',
        'wizard/validate_view.xml',
        # 'wizard/wizard_print_shift.xml',
        'views/menu.xml',
        # 'report/report_shift.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

}