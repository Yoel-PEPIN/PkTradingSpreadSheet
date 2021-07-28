# -*- coding: utf-8 -*-
#################################################################################
# Author      : Digitom (<www.digitom.fr>)
# Copyright(c): 2018-Present Digitom
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

{
    'name': "Digitom",
    'summary': "Module spécifique à KYLIANE IMPORT",
    'description': """Module spécifique à KYLIANE IMPORT""",
    'author': "DIGITOM",
    'licence': "AGPL-3",
    'website': "http://www.digitom.fr",
    'category': "Uncategorized",
    'version': '14.1.0.1.0',
    'depends': ['base','sale','point_of_sale','account','web','l10n_fr_pos_cert'],
    'data': [
        'security/groups.xml',
        'views/pos_config_views.xml',
        'views/sale_view.xml',
        'views/account_invoice_view.xml',
        'views/stock_picking_view.xml',
        'views/res_company_view.xml',
        'views/product_view.xml',
        'views/res_partner_view.xml',
        'views/contact_views.xml',
        'views/new_fields_pos.xml',
        # 'views/pos.xml',
        # 'wizard/stock_picking_confirm.xml', #TODO: now we can put code in view, dot it like this see https://apps.odoo.com/apps/modules/10.0/sale_order_mass_confirm/ TO DELETE ODOO V14 already implement it
        'report/report_invoice.xml',
        'report/sale_report_template.xml',
        'report/tpimport_external_layout_standard.xml',
        'security/ir.model.access.csv',
    ],
    'qweb': ['static/src/xml/pos.xml', ],
}