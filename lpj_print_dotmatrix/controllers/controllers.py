# -*- coding: utf-8 -*-
from odoo import http

# class LpjPrintDotmatrix(http.Controller):
#     @http.route('/lpj_print_dotmatrix/lpj_print_dotmatrix/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lpj_print_dotmatrix/lpj_print_dotmatrix/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lpj_print_dotmatrix.listing', {
#             'root': '/lpj_print_dotmatrix/lpj_print_dotmatrix',
#             'objects': http.request.env['lpj_print_dotmatrix.lpj_print_dotmatrix'].search([]),
#         })

#     @http.route('/lpj_print_dotmatrix/lpj_print_dotmatrix/objects/<model("lpj_print_dotmatrix.lpj_print_dotmatrix"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lpj_print_dotmatrix.object', {
#             'object': obj
#         })