# -*- coding: utf-8 -*-

from functools import reduce

from odoo import api, fields, models


class IrActionsActWindowView(models.Model):
    _inherit = 'ir.actions.act_window.view'

    view_mode = fields.Selection(
        selection_add=[('list', 'List')],
        ondelete={'list': 'cascade'},
    )


class StockMove(models.Model):
    _inherit = "stock.move"

    price_subtotal = fields.Float(
        string="Total US$",
        compute="_compute_totals",
        readonly=True,
    )
    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Orden de compra',
        compute="_compute_totals",
        readonly=True,
    )
    invoice_ids = fields.Many2many(
        'account.move',
        string='Facturas',
        compute="_compute_totals",
        readonly=True,
        domain=[('move_type', '=', 'in_invoice')]
    )

    @api.depends('price_unit', 'product_uom_qty')
    def _compute_totals(self):
        date = (
            self._context.get('landed_cost_date')
            or self._context.get('date')
            or fields.Date.today()
        )
        currency_usd_id = self.env["res.currency"].with_context({
            'date': date,
        }).search([("name", "=", "USD")])
        landed_cost_currency_id = self.env["res.currency"].browse(
            self._context.get('landed_cost_currency_id')
        )

        for record in self:
            record.price_subtotal = record.price_unit * record.product_uom_qty
            record.purchase_order_id = record.picking_id.purchase_id
            record.invoice_ids = record.purchase_order_id.invoice_ids


class StockPicking(models.Model):
    _inherit = "stock.picking"

    landed_costs_ids = fields.Many2many(
        'stock.landed.cost',
        string='Costes de destino',
        copy=False
    )


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    total_closeouts = fields.Integer(
        string="Total de liquidaciones",
        compute="_compute_total_closeouts",
        readonly=True,
    )

    @api.depends('picking_ids')
    def _compute_total_closeouts(self):
        for record in self:
            record.total_closeouts = len(
                record._get_move_ids_without_package().ids
            )

    def _get_move_ids_without_package(self):
        self.ensure_one()
        return reduce(
            lambda p1, p2: p1 | p2.move_ids_without_package,
            self.picking_ids,
            self.env["stock.move"]
        )

    def action_view_closeouts_detail(self):
        move_ids = self._get_move_ids_without_package().ids
        view = self.env.ref(
            'lc_detail_and_indicators.view_move_tree_closeouts_detail'
        )
        action = self.env["ir.actions.actions"]._for_xml_id(
            "lc_detail_and_indicators.closeouts_detail_action_window"
        )

        return dict(
            action,
            view_type='list',
            # view_id=view.id,
            # views=[
            #     [view.id, 'list'],
            #     # [False, 'form']
            # ],
            domain=[('id', 'in', move_ids)],
            context=dict(
                self.env.context,
                landed_cost_date=self.date,
                landed_cost_currency_id=self.currency_id.id,
            )
        )
