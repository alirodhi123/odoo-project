# -*- coding: utf-8 -*-
from odoo import http

# class TrainingOdoo(http.Controller):
#     @http.route('/training_odoo/training_odoo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/training_odoo/training_odoo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('training_odoo.listing', {
#             'root': '/training_odoo/training_odoo',
#             'objects': http.request.env['training_odoo.training_odoo'].search([]),
#         })

#     @http.route('/training_odoo/training_odoo/objects/<model("training_odoo.training_odoo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('training_odoo.object', {
#             'object': obj
#         })