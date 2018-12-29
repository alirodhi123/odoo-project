# -*- coding: utf-8 -*-
from odoo import http

# class LpjAccounting(http.Controller):
#     @http.route('/lpj_accounting/lpj_accounting/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lpj_accounting/lpj_accounting/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lpj_accounting.listing', {
#             'root': '/lpj_accounting/lpj_accounting',
#             'objects': http.request.env['lpj_accounting.lpj_accounting'].search([]),
#         })

#     @http.route('/lpj_accounting/lpj_accounting/objects/<model("lpj_accounting.lpj_accounting"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lpj_accounting.object', {
#             'object': obj
#         })