# -*- coding: utf-8 -*-
from odoo import http

# class BelajarContext(http.Controller):
#     @http.route('/belajar_context/belajar_context/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/belajar_context/belajar_context/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('belajar_context.listing', {
#             'root': '/belajar_context/belajar_context',
#             'objects': http.request.env['belajar_context.belajar_context'].search([]),
#         })

#     @http.route('/belajar_context/belajar_context/objects/<model("belajar_context.belajar_context"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('belajar_context.object', {
#             'object': obj
#         })