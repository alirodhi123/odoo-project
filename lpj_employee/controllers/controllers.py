# -*- coding: utf-8 -*-
from odoo import http

# class LpjEmployee(http.Controller):
#     @http.route('/lpj_employee/lpj_employee/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lpj_employee/lpj_employee/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lpj_employee.listing', {
#             'root': '/lpj_employee/lpj_employee',
#             'objects': http.request.env['lpj_employee.lpj_employee'].search([]),
#         })

#     @http.route('/lpj_employee/lpj_employee/objects/<model("lpj_employee.lpj_employee"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lpj_employee.object', {
#             'object': obj
#         })