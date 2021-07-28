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
from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    display_own_sales_order = fields.Boolean("Display Own Sales Order")
    sale_order_operations = fields.Selection([('draft', 'Quotations'),
                                              ('confirm', 'Confirm'), ('paid', 'Paid')], "Operation", default="draft")
    sale_order_invoice = fields.Boolean("Invoice")
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
