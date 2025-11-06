# -*- coding: utf-8 -*- 
{
    'name': 'SGEEDE Rebrand',
    'category': 'Hidden',
    'version': '1.0',
    'author': "SGEEDE",
    'website': "https://www.sgeede.com/", 
    'description':
        """
SGEEDE Enterprise Web Client.
===========================

This module is SGEEDE's Enterprise Web Client.
        """,
    'depends': ['base', 'web', 'mail', 'web_enterprise'],
    'installable': True,
    'auto_install': True,
    'data': [
        'security/ir.model.access.csv',
        'views/webclient_templates.xml',
        'wizard/sgeede_views.xml',
    ],
    'qweb': [
    ],
    'assets': {
        'web.assets_backend': [
            '/sgeede_rebrand/static/src/js/core/**/*',
            '/sgeede_rebrand/static/src/js/webclient/webclient.js',
        ]
    },
    'license': '',
}
