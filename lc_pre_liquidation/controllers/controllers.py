# -*- coding: utf-8 -*-
# from odoo import http


# class LcPreLiquidation(http.Controller):
#     @http.route('/lc_pre_liquidation/lc_pre_liquidation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lc_pre_liquidation/lc_pre_liquidation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('lc_pre_liquidation.listing', {
#             'root': '/lc_pre_liquidation/lc_pre_liquidation',
#             'objects': http.request.env['lc_pre_liquidation.lc_pre_liquidation'].search([]),
#         })

#     @http.route('/lc_pre_liquidation/lc_pre_liquidation/objects/<model("lc_pre_liquidation.lc_pre_liquidation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lc_pre_liquidation.object', {
#             'object': obj
#         })
