# -*- coding: utf-8 -*-
from odoo import http

# class Training(http.Controller):
#     @http.route('/training/training/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/training/training/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('training.listing', {
#             'root': '/training/training',
#             'objects': http.request.env['training.training'].search([]),
#         })

#     @http.route('/training/training/objects/<model("training.training"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('training.object', {
#             'object': obj
#         })