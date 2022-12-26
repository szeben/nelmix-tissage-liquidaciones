# -*- coding: utf-8 -*-
# from odoo import http


# class LcSuppliers(http.Controller):
#     @http.route('/lc_suppliers/lc_suppliers', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lc_suppliers/lc_suppliers/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('lc_suppliers.listing', {
#             'root': '/lc_suppliers/lc_suppliers',
#             'objects': http.request.env['lc_suppliers.lc_suppliers'].search([]),
#         })

#     @http.route('/lc_suppliers/lc_suppliers/objects/<model("lc_suppliers.lc_suppliers"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lc_suppliers.object', {
#             'object': obj
#         })
