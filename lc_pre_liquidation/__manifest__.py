# -*- coding: utf-8 -*-
{
    'name': "Visualización de suplidores relacionados a una liquidación",

    'summary': """
        Permite la visualización de los suplidores relacionados a una 
        liquidación, desde la misma vista del documento""",

    'description': """
        Permite la visualización de los suplidores relacionados a una 
        liquidación, desde la misma vista del documento. Los suplidores 
        son listados de acuerdo a las facturas asociadas al coste en 
        destino o liquidación
    """,

    'author': "Techne Studio IT & Consulting",
    'website': "https://technestudioit.com/",

    'license': "Other proprietary",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Stock',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'stock_landed_costs', 'lc_detail_and_indicators'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/stock_landed_cost_security.xml',
        'data/stock_landed_cost_data.xml',
        # 'views/account_move_views.xml',
        'views/stock_landed_cost_views.xml',
        # 'views/stock_valuation_layer_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
