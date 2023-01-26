# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockLandedCostLine(models.Model):
    _name = 'pre.stock.landed.cost.lines'
    _description = 'Landed Cost Lines'
    _inherit = 'stock.landed.cost.lines'

    cost_id = fields.Many2one(
        'pre.stock.landed.cost',
        string='Landed Cost',
        required=True,
        ondelete='cascade'
    )
