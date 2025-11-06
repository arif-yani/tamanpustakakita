# -*- coding: utf-8 -*-
{
    'name': 'Swiss Bakery Custom',
    'category': 'Uncategorized', 
    'author': 'Secret', 
    'version': '2.0',
    'website': '',
    'summary': 'Swiss Bakery Custom',
    'description': """ Swiss Bakery Custom """,
    'depends': ['point_of_sale'],
    'license': 'LGPL-3',
    'installable': True,
    'data': [
        'security/ir.model.access.csv',

        # 'data/menu.xml',

        'report/cashier_deposit_report.xml',
        'report/head_shop_report.xml',
        'report/store_deposit_report.xml',

        'views/sale_order_views.xml',
        'views/pos_payment_views.xml',
        'views/swiss_report.xml',

        'wizard/head_shop_wizard.xml',
        'wizard/store_deposit_wizard.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'swiss_custom/static/src/app/**/*',
            # 'swiss_custom/static/src/app/overrides/components/payment_screen/payment_screen.js',
            # 'swiss_custom/static/src/app/overrides/components/payment_screen/payment_screen.xml',
            # 'swiss_custom/static/src/app/overrides/models/models.js',
            # 'swiss_custom/static/src/app/overrides/store/pos_store.js',
        ],
    },
}
