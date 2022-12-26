# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Print Landed Cost in Odoo',
    'version': '15.0.0.0',
    'category': 'Stock',
    'summary': 'Allow to print pdf report of Landed Costo.',
    'description': """
    Allow to print pdf report of Landed Cost.
  
""",
    'price': 000,
    'currency': 'USD',
    'author': 'Astra Tech SRL',
    'website': 'https://astratech.com.do',
    'depends': ['stock_landed_costs', 'landed_cost_vo'],
    'data': [
            'report/report_stock_landed_costs.xml',
            'report/report_stock_landed_costs_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
