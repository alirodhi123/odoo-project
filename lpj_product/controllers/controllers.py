# -*- coding: utf-8 -*-
from odoo import http

# class LpjProduct(http.Controller):
#     @http.route('/lpj_product/lpj_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lpj_product/lpj_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lpj_product.listing', {
#             'root': '/lpj_product/lpj_product',
#             'objects': http.request.env['lpj_product.lpj_product'].search([]),
#         })

#     @http.route('/lpj_product/lpj_product/objects/<model("lpj_product.lpj_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lpj_product.object', {
#             'object': obj
#         })