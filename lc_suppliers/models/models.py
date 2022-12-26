# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    total_suppliers = fields.Integer(
        compute="_compute_total_suppliers",
        store=True,
        readonly=True
    )

    @api.depends("vendor_bill_ids.partner_id")
    def _compute_total_suppliers(self):
        for record in self:
            record.total_suppliers = len(record.vendor_bill_ids.partner_id.ids)

    def action_view_suppliers(self):
        self.ensure_one()
        domain = [('id', 'in', self.vendor_bill_ids.partner_id.ids)]
        action = self.env["ir.actions.actions"]._for_xml_id(
            "contacts.action_contacts"
        )
        return dict(
            action,
            display_name="Suplidores",
            view_type='list',
            view_mode='list',
            views=[[False, 'list'], [False, 'form']],
            domain=domain,
        )
