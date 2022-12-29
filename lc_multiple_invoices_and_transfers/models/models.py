# -*- coding: utf-8 -*-

from collections import defaultdict
from functools import reduce

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_is_zero


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    vendor_bill_id = None
    vendor_bill_ids = fields.Many2many(
        'account.move',
        string='Vendor Bills',
        copy=False,
        domain=[('move_type', '=', 'in_invoice')]
    )

    def button_validate(self):
        self._check_can_validate()
        cost_without_adjusment_lines = self.filtered(
            lambda c: not c.valuation_adjustment_lines
        )
        if cost_without_adjusment_lines:
            cost_without_adjusment_lines.compute_landed_cost()
        if not self._check_sum():
            raise UserError(
                _('Cost and adjustments lines do not match. You should maybe recompute the landed costs.')
            )

        for cost in self:
            cost = cost.with_company(cost.company_id)
            move = self.env['account.move']
            move_vals = {
                'journal_id': cost.account_journal_id.id,
                'date': cost.date,
                'ref': cost.name,
                'line_ids': [],
                'move_type': 'entry',
            }
            valuation_layer_ids = []
            cost_to_add_byproduct = defaultdict(lambda: 0.0)
            for line in cost.valuation_adjustment_lines.filtered(lambda line: line.move_id):
                remaining_qty = sum(
                    line.move_id.stock_valuation_layer_ids.mapped(
                        'remaining_qty'
                    )
                )
                linked_layer = line.move_id.stock_valuation_layer_ids[:1]

                # Prorate the value at what's still in stock
                cost_to_add = (
                    remaining_qty / line.move_id.product_qty
                ) * line.additional_landed_cost
                if not cost.company_id.currency_id.is_zero(cost_to_add):
                    valuation_layer = self.env['stock.valuation.layer'].create({
                        'value': cost_to_add,
                        'unit_cost': 0,
                        'quantity': 0,
                        'remaining_qty': 0,
                        'stock_valuation_layer_id': linked_layer.id,
                        'description': cost.name,
                        'stock_move_id': line.move_id.id,
                        'product_id': line.move_id.product_id.id,
                        'stock_landed_cost_id': cost.id,
                        'company_id': cost.company_id.id,
                    })
                    linked_layer.remaining_value += cost_to_add
                    valuation_layer_ids.append(valuation_layer.id)
                # Update the AVCO
                product = line.move_id.product_id
                if product.cost_method == 'average':
                    cost_to_add_byproduct[product] += cost_to_add
                # Products with manual inventory valuation are ignored because they do not need to create journal entries.
                if product.valuation != "real_time":
                    continue
                # `remaining_qty` is negative if the move is out and delivered proudcts that were not
                # in stock.
                qty_out = 0
                if line.move_id._is_in():
                    qty_out = line.move_id.product_qty - remaining_qty
                elif line.move_id._is_out():
                    qty_out = line.move_id.product_qty
                move_vals['line_ids'] += line._create_accounting_entries(
                    move, qty_out)

            # batch standard price computation avoid recompute quantity_svl at each iteration
            products = self.env['product.product'].browse(
                p.id for p in cost_to_add_byproduct.keys()
            )
            for product in products:  # iterate on recordset to prefetch efficiently quantity_svl
                if not float_is_zero(product.quantity_svl, precision_rounding=product.uom_id.rounding):
                    product.with_company(cost.company_id).sudo().with_context(
                        disable_auto_svl=True).standard_price += cost_to_add_byproduct[product] / product.quantity_svl

            move_vals['stock_valuation_layer_ids'] = [
                (6, None, valuation_layer_ids)
            ]
            # We will only create the accounting entry when there are defined lines (the lines will be those linked to products of real_time valuation category).
            cost_vals = {'state': 'done'}
            if move_vals.get("line_ids"):
                move = move.create(move_vals)
                cost_vals.update({'account_move_id': move.id})
            cost.write(cost_vals)
            if cost.account_move_id:
                move._post()

            vendor_bill_ids = cost.vendor_bill_ids.filtered(
                lambda bill: bill.state == 'posted'
            )

            if vendor_bill_ids and cost.company_id.anglo_saxon_accounting:
                all_amls = reduce(
                    lambda b1, b2: b1 | b2.line_ids,
                    vendor_bill_ids,
                    self.env['account.move.line']
                ) | cost.account_move_id.line_ids

                for product in cost.cost_lines.product_id:
                    accounts = product.product_tmpl_id.get_product_accounts()
                    input_account = accounts['stock_input']
                    all_amls.filtered(
                        lambda aml: aml.account_id == input_account and not aml.full_reconcile_id
                    ).reconcile()

        return True


class AccountMove(models.Model):
    _inherit = 'account.move'

    landed_costs_ids = fields.Many2many(
        'stock.landed.cost',
        string='Landed Costs'
    )

    def button_create_landed_costs(self):
        self.ensure_one()
        landed_costs_lines = self.line_ids.filtered(
            lambda line: line.is_landed_costs_line
        )

        landed_costs = self.env['stock.landed.cost'].create({
            'vendor_bill_ids': [(4, 0, self.id)],
            'cost_lines': [(0, 0, {
                'product_id': l.product_id.id,
                'name': l.product_id.name,
                'account_id': l.product_id.product_tmpl_id.get_product_accounts()['stock_input'].id,
                'price_unit': l.currency_id._convert(l.price_subtotal, l.company_currency_id, l.company_id, l.move_id.date),
                'split_method': l.product_id.split_method_landed_cost or 'equal',
            }) for l in landed_costs_lines],
        })
        action = self.env["ir.actions.actions"]._for_xml_id(
            "stock_landed_costs.action_stock_landed_cost"
        )
        return dict(action, view_mode='form', res_id=landed_costs.id, views=[(False, 'form')])

    def action_view_landed_costs(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "stock_landed_costs.action_stock_landed_cost"
        )
        domain = [('id', 'in', self.landed_costs_ids.ids)]
        context = dict(
            self.env.context,
            default_vendor_bill_ids=[(4, 0, i) for i in self.ids]
        )
        views = [
            (self.env.ref('stock_landed_costs.view_stock_landed_cost_tree2').id, 'tree'),
            (False, 'form'),
            (False, 'kanban')
        ]
        return dict(action, domain=domain, context=context, views=views)
