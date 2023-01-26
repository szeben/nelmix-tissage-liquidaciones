# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockLandedCostProductLine(models.Model):
    _name = 'pre.stock.landed.cost.product.lines'
    _description = 'Landed Cost Product Lines'

    def _default_currency(self):
        if self.product_id:
            return self.product_id.currency_id
        return self.env.company.currency_id

    cost_id = fields.Many2one(
        'pre.stock.landed.cost',
        string='Landed Cost',
        required=True,
        ondelete='cascade'
    )
    product_id = fields.Many2one(
        'product.product',
        string='Producto',
        required=True
    )
    quantity = fields.Float(
        string='Cantidad',
        required=True,
        default=1.0
    )
    price_unit = fields.Monetary(
        string='Precio Unitario',
        currency_field='currency_id',
        required=True
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        default=_default_currency
    )

    # Details
    total = fields.Float(
        string='Total',
        compute='_compute_total',
        store=True
    )
    item = fields.Integer(
        string="Item",
        compute="_compute_totals",
        readonly=True,
    )
    currency_rate_usd = fields.Float(
        string="Tasa USD",
        related="cost_id.currency_rate_usd",
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
        default=lambda self: self.product_id.lst_price
    )
    pvp_rd = fields.Float(
        string="PVP RD",
        compute="_compute_pvp",
        compute_sudo=True,
        readonly=True,
    )
    margin = fields.Float(
        string="Margen %",
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

    @api.depends('quantity', 'price_unit')
    def _compute_total(self):
        for line in self:
            line.total = line.quantity * line.price_unit

    @api.depends('currency_rate_usd', 'price_unit', 'quantity')
    def _compute_totals(self):
        for item, record in enumerate(self, start=1):
            record.item = item
            record.price_subtotal = record.price_unit * record.quantity
            record.price_unit_rd = record.price_unit * record.currency_rate_usd
            record.amount_total_rd = record.price_unit_rd * record.quantity

    @api.depends('cost_id.amount_total', 'price_subtotal', 'amount_total_rd')
    def _compute_factor(self):
        total_usd = sum(self.mapped('price_subtotal'))
        total_rd = sum(self.mapped('amount_total_rd'))
        if total_usd:
            self.factor = (self.cost_id.amount_total + total_rd) / total_usd
        else:
            self.factor = 1.0

    @api.depends('currency_rate_usd', 'factor', 'quantity')
    def _compute_current_totals(self):
        for record in self:
            record.current_price_unit_rd = record.price_unit_rd * record.factor
            record.current_total_rd = record.current_price_unit_rd * record.quantity
            record.current_price_unit_usd = (
                record.current_price_unit_rd / record.currency_rate_usd
                if record.currency_rate_usd else 0.0
            )
            record.current_total_usd = record.current_price_unit_usd * record.quantity

    @api.depends('currency_rate_usd', 'pvp_usd')
    def _compute_pvp(self):
        for record in self:
            record.pvp_rd = record.pvp_usd * record.currency_rate_usd

    @api.depends('pvp_usd', 'pvp_rd', 'current_price_unit_usd', 'current_price_unit_rd', 'quantity')
    def _compute_extra_indicators(self):
        for record in self:
            if record.pvp_usd:
                record.margin = (record.pvp_usd - record.current_price_unit_usd) * 100 / record.pvp_usd
            else:
                record.margin = 0.0
            record.profit_usd = (record.pvp_usd - record.current_price_unit_usd) * record.quantity
            record.profit_rd = (record.pvp_rd - record.current_price_unit_rd) * record.quantity

    def get_lst_price_from_product(self, vals):
        pvp_usd = vals.get('pvp_usd')

        if not pvp_usd:
            product = self.env['product.product'].browse(vals.get('product_id'))
            pvp_usd = product.lst_price

        return pvp_usd

    @api.model
    def create(self, vals_list):
        if isinstance(vals_list, dict):
            vals_list['pvp_usd'] = self.get_lst_price_from_product(vals_list)
        else:
            for vals in vals_list:
                vals['pvp_usd'] = self.get_lst_price_from_product(vals)
        return super().create(vals_list)
