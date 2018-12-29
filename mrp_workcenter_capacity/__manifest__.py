# -*- coding: utf-8 -*-
# Copyright (c) Open Value All Rights Reserved                     
# License LGPL-3 or later (https://www.gnu.org/licenses/).

{
    "name": "Work Center Capacity",
    "summary": 'Production Work Center Capacity Calculation',
    "version": "10.0.1.0.0",
    "category": "Manufacturing",
    "website": '',
    "author": "Open Value",
    "support": 'opentechvalue@gmail.com',
    "license": "LGPL-3",
    "price": 00.00,
    "currency": 'EUR',
    "depends": [
        "mrp", 
    ],
    "data": [
        "views/mrp_workcenter_capacity_view.xml",
        "views/mrp_workcenter_tree_view.xml",
        "views/mrp_workorder_capacity_view.xml"
    ],
    "application": False,
    "installable": True,
    "auto_install": False, 
}

