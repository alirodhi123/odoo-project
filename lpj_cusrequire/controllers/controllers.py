# -*- coding: utf-8 -*-
from odoo import http

# class LpjCusrequire(http.Controller):
#     @http.route('/lpj_cusrequire/lpj_cusrequire/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lpj_cusrequire/lpj_cusrequire/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lpj_cusrequire.listing', {
#             'root': '/lpj_cusrequire/lpj_cusrequire',
#             'objects': http.request.env['lpj_cusrequire.lpj_cusrequire'].search([]),
#         })

#     @http.route('/lpj_cusrequire/lpj_cusrequire/objects/<model("lpj_cusrequire.lpj_cusrequire"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lpj_cusrequire.object', {
#             'object': obj
#         })