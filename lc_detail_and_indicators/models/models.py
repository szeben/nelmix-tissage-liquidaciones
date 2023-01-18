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

    item = fields.Integer(
        string="Item",
        compute="_compute_totals",
        readonly=True,
    )
    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Orden de compra',
        compute="_compute_info_purchase",
        store=True,
        readonly=True,
    )
    supplier_id = fields.Many2one(
        'res.partner',
        string='Proveedor',
        compute="_compute_info_purchase",
        store=True,
        readonly=True,
    )
    invoice_ids = fields.Many2many(
        'account.move',
        string='Facturas',
        compute="_compute_info_purchase",
        store=True,
        readonly=True,
        domain=[('move_type', '=', 'in_invoice')]
    )
    currency_rate_usd = fields.Float(
        string="Tasa USD",
        compute="_compute_rate_usd",
        readonly=True,
    )
    price_subtotal = fields.Float(
        string="Total US$",
        compute="_compute_totals",
        readonly=True,
    )
    price_unit_rd = fields.Float(
        string="C/U RD",
        compute="_compute_totals",
        readonly=True,
    )
    amount_total_rd = fields.Float(
        string="Total RD",
        compute="_compute_totals",
        readonly=True,
    )
    factor = fields.Float(
        string="Factor",
        compute="_compute_factor",
        readonly=True,
    )
    current_price_unit_rd = fields.Float(
        string="C/U Actual RD",
        compute="_compute_current_totals",
        readonly=True,
    )
    current_total_rd = fields.Float(
        string="C/T Actual RD",
        compute="_compute_current_totals",
        readonly=True,
    )
    current_price_unit_usd = fields.Float(
        string="C/U Actual US$",
        compute="_compute_current_totals",
        readonly=True,
    )
    current_total_usd = fields.Float(
        string="C/T Actual US$",
        compute="_compute_current_totals",
        readonly=True,
    )
    pvp_usd = fields.Float(
        string="PVP US$",
        default=lambda self: self.product_id.lst_price,
        store=True,
    )
    pvp_rd = fields.Float(
        string="PVP RD",
        compute="_compute_pvp",
        compute_sudo=True,
        readonly=True,
    )
    margin = fields.Float(
        string="Margen",
        compute="_compute_extra_indicators",
        readonly=True,
    )
    profit_usd = fields.Float(
        string="Ganancias en US$",
        compute="_compute_extra_indicators",
        readonly=True,
    )
    profit_rd = fields.Float(
        string="Ganancias en RD",
        compute="_compute_extra_indicators",
        readonly=True,
    )

    @api.depends_context('landed_cost_date', 'date')
    def _compute_rate_usd(self):
        date = (
            self._context.get('landed_cost_date')
            or self._context.get('date')
            or fields.Date.today()
        )
        self.currency_rate_usd = self.env["res.currency"].with_context({
            'date': date,
        }).search([("name", "=", "USD")]).rate

    @api.onchange('product_id', 'product_id.lst_price')
    def _onchange_product_lst_price(self):
        for record in self:
            record.pvp_usd = record.product_id.lst_price

    @api.depends('picking_id', 'picking_id.purchase_id', 'picking_id.purchase_id.invoice_ids')
    def _compute_info_purchase(self):
        for record in self:
            record.purchase_order_id = record.picking_id.purchase_id
            record.invoice_ids = record.picking_id.purchase_id.invoice_ids
            record.supplier_id = record.picking_id.partner_id

    @api.depends('currency_rate_usd', 'price_unit', 'product_uom_qty')
    def _compute_totals(self):
        for item, record in enumerate(self, start=1):
            record.item = item
            record.price_subtotal = record.price_unit * record.product_uom_qty
            record.price_unit_rd = record.price_unit * record.currency_rate_usd
            record.amount_total_rd = record.price_unit_rd * record.product_uom_qty

    @api.depends('price_subtotal', 'amount_total_rd')
    @api.depends_context('landed_cost_id')
    def _compute_factor(self):
        landed_cost = self.env['stock.landed.cost'].browse(
            self._context.get('landed_cost_id') or self._context.get('active_id')
        )

        if landed_cost:
            total_usd = sum(self.mapped('price_subtotal'))
            total_rd = sum(self.mapped('amount_total_rd'))
            self.factor = (landed_cost.amount_total + total_rd) / total_usd
        else:
            self.factor = 1.0

    @api.depends('currency_rate_usd', 'factor')
    def _compute_current_totals(self):
        for record in self:
            record.current_price_unit_rd = record.price_unit_rd * record.factor
            record.current_total_rd = record.current_price_unit_rd * record.product_uom_qty
            record.current_price_unit_usd = record.current_price_unit_rd / record.currency_rate_usd
            record.current_total_usd = record.current_price_unit_usd * record.product_uom_qty

    @api.depends('currency_rate_usd', 'pvp_usd')
    def _compute_pvp(self):
        for record in self:
            record.pvp_rd = record.pvp_usd * record.currency_rate_usd

    @api.depends('pvp_usd', 'pvp_rd', 'current_price_unit_usd', 'current_price_unit_rd', 'product_uom_qty')
    def _compute_extra_indicators(self):
        for record in self:
            record.margin = (record.pvp_usd - record.current_price_unit_usd) * 100 / record.pvp_usd
            record.profit_usd = (record.pvp_usd - record.current_price_unit_usd) * record.product_uom_qty
            record.profit_rd = (record.pvp_rd - record.current_price_unit_rd) * record.product_uom_qty


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
        action = self.env["ir.actions.actions"]._for_xml_id(
            "lc_detail_and_indicators.closeouts_detail_action_window"
        )

        return dict(
            action,
            view_type='list',
            domain=[('id', 'in', move_ids)],
            context=dict(
                self.env.context,
                landed_cost_id=self.id,
                landed_cost_date=self.date
            )
        )
