# -*- coding: utf-8 -*-
from odoo import http

# class LpjAttendance(http.Controller):
#     @http.route('/lpj_attendance/lpj_attendance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lpj_attendance/lpj_attendance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lpj_attendance.listing', {
#             'root': '/lpj_attendance/lpj_attendance',
#             'objects': http.request.env['lpj_attendance.lpj_attendance'].search([]),
#         })

#     @http.route('/lpj_attendance/lpj_attendance/objects/<model("lpj_attendance.lpj_attendance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lpj_attendance.object', {
#             'object': obj
#         })