# -*- coding: utf-8 -*-
from odoo import http

# class LpjTraining(http.Controller):
#     @http.route('/lpj_training/lpj_training/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lpj_training/lpj_training/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lpj_training.listing', {
#             'root': '/lpj_training/lpj_training',
#             'objects': http.request.env['lpj_training.lpj_training'].search([]),
#         })

#     @http.route('/lpj_training/lpj_training/objects/<model("lpj_training.lpj_training"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lpj_training.object', {
#             'object': obj
#         })