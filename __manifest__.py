# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'Odoo POS Offers',
    'version': '15.0.1.0.0',
    'summary': """Add offers to products that are to be sold to in the POS""",
    'description': """"This module helps you add offers with a date range and link the offers to products then view the products on the POS.""",
    'category': 'POS',
    'author': 'Gkarumba',
    'company': 'Gkarumba',
    'website': "gachegua@gmail.com",
    'depends': ['base', 'project', 'hr_timesheet'],
    'data': [
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
        "security/security.xml",
        "data/ir_cron.xml",
        "views/menus.xml",
        "views/offers.xml",
        "views/product.xml",
        ],
    'assets': {},
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}