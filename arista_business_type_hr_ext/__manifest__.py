# -*- coding: utf-8 -*-
{
    'name': 'HR Multi-channels',
    'version': '13.0.1.0.0',
    'license': 'OPL-1',
    'summary': 'Add business type object in HR',
    'category': 'Inventory',
    'author': "CLuedoo",
    'website': "https://www.cluedoo.com",
    'support': 'cluedoo@falinwa.com',
    'description':
    '''
        HR Business Type
        ===================

        Add business type in stock to manage multiple sequence
    ''',
    'depends': [
        'hr_payroll',
        'hr_payroll_account',
        'fal_business_type_invoice_ext',
    ],
    'data': [
        'security/hr_business_security.xml',
        # 'views/hr_payroll_structure_views.xml',
        'views/hr_payslip_views.xml',
        # 'views/stock_warehouse_views.xml',
        # 'views/stock_picking_views.xml',
    ],
    'images': [
        # 'static/description/crm_business_type_screenshot.png'
    ],
    'demo': [
    ],
    'price': 270.00,
    'currency': 'EUR',
    'application': False,
}
