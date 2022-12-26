# -*- coding: utf-8 -*-
# from odoo import http


# class LcMultipleInvoicesAndTransfers(http.Controller):
#     @http.route('/lc_multiple_invoices_and_transfers/lc_multiple_invoices_and_transfers', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lc_multiple_invoices_and_transfers/lc_multiple_invoices_and_transfers/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('lc_multiple_invoices_and_transfers.listing', {
#             'root': '/lc_multiple_invoices_and_transfers/lc_multiple_invoices_and_transfers',
#             'objects': http.request.env['lc_multiple_invoices_and_transfers.lc_multiple_invoices_and_transfers'].search([]),
#         })

#     @http.route('/lc_multiple_invoices_and_transfers/lc_multiple_invoices_and_transfers/objects/<model("lc_multiple_invoices_and_transfers.lc_multiple_invoices_and_transfers"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lc_multiple_invoices_and_transfers.object', {
#             'object': obj
#         })
