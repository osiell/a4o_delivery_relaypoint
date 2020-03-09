# -*- coding: utf-8 -*-
# This file is part of an Adiczion's Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
{
    'name': 'Module Delivery Relay Points',
    'version': '12.0.0',
    'author': 'Adiczion SARL',
    'category': 'Adiczion',
    'license': 'AGPL-3',
    'depends': [
        'stock',
        'delivery',
    ],
    'demo': [],
    'website': 'http://adiczion.com',
    'description': """
Module Delivery Relay Points
============================

[Add the description of your module here].

    """,
    'data': [
        'security/objects_security.xml',
        'security/ir.model.access.csv',
        'wizard/select_relaypoint_views.xml',
        #'data/data_for_your_module.xml',
        #'views/view_of_your_module.xml',
    ],
    'images': ['static/description/banner.png'],
    'test': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: