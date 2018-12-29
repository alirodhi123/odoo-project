# -*- coding: utf-8 -*-
from odoo import http

# class LpjCalendar(http.Controller):
#     @http.route('/lpj_calendar/lpj_calendar/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lpj_calendar/lpj_calendar/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lpj_calendar.listing', {
#             'root': '/lpj_calendar/lpj_calendar',
#             'objects': http.request.env['lpj_calendar.lpj_calendar'].search([]),
#         })

#     @http.route('/lpj_calendar/lpj_calendar/objects/<model("lpj_calendar.lpj_calendar"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lpj_calendar.object', {
#             'object': obj
#         })