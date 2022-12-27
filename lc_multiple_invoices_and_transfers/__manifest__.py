# -*- coding: utf-8 -*-
{
    'name': "Asociación de múltiples facturas y transferencias a coste en destino",

    'summary': """
        Permite la selección y asociación de múltiples facturas y transferencias de 
        inventario a un documento de Liquidación o coste en destino""",

    'description': """
        Permite la selección y asociación de múltiples facturas y transferencias de 
        inventario a un documento de Liquidación o coste en destino, permitiendo 
        además la consulta directa del documento asociado
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
    'depends': ['base', 'account', 'stock', 'stock_landed_costs'],

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
