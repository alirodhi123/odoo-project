# -*- coding: utf-8 -*-
from odoo import http

# class LpjPerformanceManagement(http.Controller):
#     @http.route('/lpj_performance_management/lpj_performance_management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lpj_performance_management/lpj_performance_management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lpj_performance_management.listing', {
#             'root': '/lpj_performance_management/lpj_performance_management',
#             'objects': http.request.env['lpj_performance_management.lpj_performance_management'].search([]),
#         })

#     @http.route('/lpj_performance_management/lpj_performance_management/objects/<model("lpj_performance_management.lpj_performance_management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lpj_performance_management.object', {
#             'object': obj
#         })