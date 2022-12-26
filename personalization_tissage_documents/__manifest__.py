# -*- coding: utf-8 -*-
{
    'name': "Personalización de documentos Tissage",

    'summary': """
        Personalización de documentos Tissage.""",

    'description': """
        Personalización de documentos a estilo Tissage: Cotización, factura de venta y conduce.    """,

    'author': "Techne Studio IT & Consulting",
    'website': "https://technestudioit.com/",

    'license': "Other proprietary",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'account', 'stock'],

    # always loaded
    'data': [
        'report/sale_action_report_saleorder_custom.xml',
        'report/sale_report_templates_custom.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
