# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2017 vitraining.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
##############################################################################

{
    "name": "MRP Production Cost",
    "version": "2.0",
    "author" : "vitraining.com",
    "website": "www.vitraining.com",
    "description": """
    
Functionalities:
 - Calculates the production cost price from the actual price of the components
 - Assigns a picking for consumed materials

Based on deltatech_mrp_cost with modifications on the calculation method.


Find our other interesting modules that can make your life easier:
https://www.odoo.com/apps/modules/browse?search=vitraining
        
        
    """,

    "category": "Manufacturing",
    "depends": [
        "mrp", "stock",
        "sale",
        "product",

    ],

    "data": [
        "views/mrp_view.xml",
        "data/mrp_data.xml"
    ],
    "active": False,
    "installable": True,
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
