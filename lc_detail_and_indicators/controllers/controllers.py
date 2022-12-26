# -*- coding: utf-8 -*-
# from odoo import http


# class LcDetailAndIndicators(http.Controller):
#     @http.route('/lc_detail_and_indicators/lc_detail_and_indicators', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lc_detail_and_indicators/lc_detail_and_indicators/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('lc_detail_and_indicators.listing', {
#             'root': '/lc_detail_and_indicators/lc_detail_and_indicators',
#             'objects': http.request.env['lc_detail_and_indicators.lc_detail_and_indicators'].search([]),
#         })

#     @http.route('/lc_detail_and_indicators/lc_detail_and_indicators/objects/<model("lc_detail_and_indicators.lc_detail_and_indicators"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lc_detail_and_indicators.object', {
#             'object': obj
#         })
