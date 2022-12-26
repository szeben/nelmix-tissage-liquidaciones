# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class lc_pre_liquidation(models.Model):
#     _name = 'lc_pre_liquidation.lc_pre_liquidation'
#     _description = 'lc_pre_liquidation.lc_pre_liquidation'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
