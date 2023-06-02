# -*- coding: utf-8 -*-
{
    'name': "point of sale devise",
    'summary': """,
    custom pos""",
    'description': """
        custom pos
    """,

    'author': "progistack",
    'website': "https://www.progistack.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/pos_config_view_inherit.xml',
        'views/res_config_settings_view_inherit.xml',
    ],
    'assets': {
                'point_of_sale.assets': [
                    'pos_custome/static/src/js/inherit_models.js',
                    'pos_custome/static/src/js/inherit_orderSummary.js',
                    'pos_custome/static/src/xml/InheritOrderSummary.xml',
                    'pos_custome/static/src/xml/inheritCashMovePopup.xml',
                    'pos_custome/static/src/js/inherit_CashMovePopup.js',
                    'pos_custome/static/src/xml/inheritClosePopup.xml',
                    'pos_custome/static/src/css/popup/closing_popup.css',
                    # 'pos_custome/static/src/js/inherit_closePopup.js',
                    
                ],
            },
}
