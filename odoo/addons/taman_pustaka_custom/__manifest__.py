{
    'name': 'Taman Pustaka Kita Custom Module',
    'version': '1.0',
    'author': 'Arif',
    'summary': 'Taman Pustaka Kita Custom Module',
    'description': """
        Taman Pustaka Kita Custom Module
    """,
    'website': 'https://www.sgeede.com',
    'depends': ['account', 'product'],
    'category': 'Extra Tools',
    'demo': [],
    'data': [
        'data/ir_cron.xml',
        'report/ir_action_report.xml',
        'report/invoice_report.xml',
        'views/account_move_views.xml',
        'views/product_views.xml',
        
    ],
    'assets': {
    },
    'installable': True,
    'qweb': [],
}