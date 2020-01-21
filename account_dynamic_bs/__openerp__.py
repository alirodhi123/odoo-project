# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Dynamic Balance Sheet Report',
    'version': '9.0.0.2',
    'category': 'Accounting',
    'author': 'Pycus',
    'summary': 'Dynamic Balance Sheet Report with interactive drill down view and extra filters',
    'description': """
                This module support for viewing Balance Sheet report on the screen with 
                drilldown option. Option to download report into Pdf and Xlsx

                    """,
    "price": 25,
    "currency": 'EUR',
    'depends': ['account','report_xlsx'],
    'data': [
             "views/assets.xml",
             "views/views.xml",
    ],
    'demo': [],
    'qweb':['static/src/xml/dynamic_bs_report.xml'],
    "images":['static/description/Dynamic_BS.gif'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
