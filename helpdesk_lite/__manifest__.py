# -*- coding: utf-8 -*-
{
    'name': "HelpDesk",
    'version': "0.1",
    'author': "Golubev",
    'category': "Tools",
    'support': "golubev@svami.in.ua",
    'summary': "A helpdesk / support ticket system",
    'description': "A helpdesk / support ticket system",
    'license':'LGPL-3',
    'data': [
        'security/helpdesk_security.xml',
        'security/ir.model.access.csv',
        'views/helpdesk_tickets.xml',
        'views/helpdesk_categ_view.xml',
        'views/helpdesk_categ_problem_view.xml',
        'views/templates.xml',
        'views/sequence.xml',
        'views/helpdesk_assets_view.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/helpdesk_demo.xml',
    ],
    'depends': ['base','mail', 'stock'],
    'application': True,
}
