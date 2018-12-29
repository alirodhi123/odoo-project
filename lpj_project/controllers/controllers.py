# -*- coding: utf-8 -*-
from odoo import http

# class LpjProject(http.Controller):
#     @http.route('/lpj_project/lpj_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lpj_project/lpj_project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lpj_project.listing', {
#             'root': '/lpj_project/lpj_project',
#             'objects': http.request.env['lpj_project.lpj_project'].search([]),
#         })

#     @http.route('/lpj_project/lpj_project/objects/<model("lpj_project.lpj_project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lpj_project.object', {
#             'object': obj
#         })