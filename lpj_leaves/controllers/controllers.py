# -*- coding: utf-8 -*-
from odoo import http

# class LpjLeaves(http.Controller):
#     @http.route('/lpj_leaves/lpj_leaves/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lpj_leaves/lpj_leaves/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lpj_leaves.listing', {
#             'root': '/lpj_leaves/lpj_leaves',
#             'objects': http.request.env['lpj_leaves.lpj_leaves'].search([]),
#         })

#     @http.route('/lpj_leaves/lpj_leaves/objects/<model("lpj_leaves.lpj_leaves"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lpj_leaves.object', {
#             'object': obj
#         })