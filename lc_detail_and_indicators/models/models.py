# -*- coding: utf-8 -*-

from functools import reduce
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    price_subtotal = fields.Float(
        string="Total US$",
        compute="_compute_totals",
        readonly=True,
    )

    @api.depends('price_unit', 'product_uom_qty')
    def _compute_totals(self):
        for record in self:
            record.price_subtotal = record.price_unit * record.product_uom_qty




class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    total_transfers = fields.Integer(
        string="Total de Transferencias",
        compute="_compute_total_transfers",
        # store=True,
        readonly=True,
    )

    @api.depends('picking_ids')
    def _compute_total_transfers(self):
        for record in self:
            record.total_transfers = len(
                record._get_move_ids_without_package().ids
            )

    def _get_move_ids_without_package(self):
        self.ensure_one()
        return reduce(
            lambda p1, p2: p1.move_ids_without_package | p2.move_ids_without_package,
            self.picking_ids,
            self.env["stock.picking"]
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
            view_id=view.id,
            views=[
                [view.id, 'list'],
                # [False, 'form']
            ],
            domain=[('id', 'in', move_ids)],
        )
