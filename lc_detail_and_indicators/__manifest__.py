# -*- coding: utf-8 -*-
{
    'name': "Visualización del detalle e indicadores de un coste en destino o liquidación",

    'summary': """
        Incluye una vista con el detalle del coste en destino o liquidación y 
        una pestaña con indicadores de interés""",

    'description': """
        Incluye una vista con el detalle del coste en destino o liquidación basado 
        en las transferencias asociadas al mismo. Adicionalmente incluye una pestaña 
        con indicadores de interés generados por la información del detalle del 
        coste en destino
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
    'depends': ['base', 'stock', 'purchase_stock', 'stock_landed_costs'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
