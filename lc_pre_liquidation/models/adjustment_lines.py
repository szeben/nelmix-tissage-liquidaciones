# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AdjustmentLines(models.Model):
    _name = 'pre.stock.valuation.adjustment.lines'
    _description = 'Stock Valuation Adjustment Lines'
    _inherit = 'stock.valuation.adjustment.lines'

    cost_id = fields.Many2one(
        'pre.stock.landed.cost',
        string='Landed Cost',
        ondelete='cascade', required=True
    )
    cost_line_id = fields.Many2one(
        'pre.stock.landed.cost.lines',
        string='Cost Line',
        readonly=True
    )
    additional_landed_cost = fields.Monetary(
        string='Additional Landed Cost'
    )

    @api.model
    def _add_field(self, name, field):
        if name == 'move_id':
            # ignore the field
            # move_id = fields.Many2one('stock.move', 'Stock Move', readonly=True)
            return
        return super()._add_field(name, field)

    def _create_accounting_entries(self, move, qty_out):
        # TDE CLEANME: product chosen for computation ?``
        cost_product = self.cost_line_id.product_id
        if not cost_product:
            return False

        accounts = self.product_id.product_tmpl_id.get_product_accounts()
        debit_account_id = accounts.get('stock_valuation') and accounts['stock_valuation'].id or False

        # If the stock move is dropshipped move we need to get the cost account instead the stock valuation account
        # if self.move_id and self.move_id._is_dropshipped():
        #     debit_account_id = accounts.get('expense') and accounts['expense'].id or False

        already_out_account_id = accounts['stock_output'].id
        credit_account_id = self.cost_line_id.account_id.id or cost_product.categ_id.property_stock_account_input_categ_id.id

        if not credit_account_id:
            raise UserError(_('Please configure Stock Expense Account for product: %s.') % (cost_product.name))

        return self._create_account_move_line(move, credit_account_id, debit_account_id, qty_out, already_out_account_id)
