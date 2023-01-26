# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class StockProductDetail(models.Model):
    _name = 'pre.stock.product.detail'
    _description = 'Stock Landed Cost Product Details'

    name = fields.Char(
        string=u'Descripción',
        required=True
    )
    landed_cost_id = fields.Many2one(
        comodel_name='pre.stock.landed.cost',
        string=u'Liquidación',
        ondelete='cascade',
        required=True
    )
    product_id = fields.Many2one(
        'product.product',
        string='Producto',
        required=True
    )
    quantity = fields.Float(
        string='Cantidad',
        default=1.0,
        digits=dp.get_precision('Product Unit of Measure'),
        required=True
    )
    actual_cost = fields.Float(
        string='Costo actual unitario',
        readonly=True
    )
    additional_cost = fields.Float(
        string=u'Costo de Importación',
        readonly=True
    )
    new_cost = fields.Float(
        string=u'Nuevo Costo',
        readonly=True
    )
