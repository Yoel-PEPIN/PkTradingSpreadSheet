# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
{
    "name": "Create sales order from Point of Sale with Extended Features (Community)",
    'summary': "Create sales order from Point of Sale with Extended Features",
    "version": "1.0",
    "description": """
        Create sales order from Point of Sale with Extended Features.
    """,
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'category': 'Point of Sale',
    'website': 'http://www.acespritech.com',
    'price': 120.00,
    'currency': 'EUR',
    "depends": ['sale_management', 'point_of_sale'],
    "data": [
        'views/pos_assets.xml',
        'views/point_of_sale.xml',
    ],
    'qweb': ['static/src/xml/Screens/ProductScreen/ControlButtons/CreateSaleOrderButton.xml',
             'static/src/xml/Screens/ProductScreen/ControlButtons/InvoicesButton.xml',
             'static/src/xml/Screens/ProductScreen/ControlButtons/ViewSaleOrderButton.xml',

             'static/src/xml/Screens/PaymentScreen/PaymentScreen.xml',

             'static/src/xml/Chrome.xml',
             'static/src/xml/Screens/ChromeWidgets/SaleOrderMode.xml',

             'static/src/xml/Screens/CreateSaleOrderScreen/CreateSaleOrderScreen.xml',
             'static/src/xml/Screens/CreateSaleOrderScreen/SignatureWidget.xml',

             'static/src/xml/Screens/SaleOrderScreen/SaleOrderScreen.xml',
             'static/src/xml/Screens/SaleOrderScreen/SaleOrdersLine.xml',

             'static/src/xml/Screens/InvoiceScreen/InvoiceScreen.xml',
             'static/src/xml/Screens/InvoiceScreen/InvoiceLine.xml',

             'static/src/xml/Popups/SaleOrderConfirmPopup.xml',
             'static/src/xml/Popups/SaleOrderReturnPopup.xml',
             'static/src/xml/Popups/PopupProductLines.xml',
             ],
    'images': ['static/description/main_screenshot.png'],
    "auto_install": False,
    "installable": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
