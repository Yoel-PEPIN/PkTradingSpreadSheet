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


class PosConfig(models.Model):
    _inherit = 'pos.config'

    paid_amount_product = fields.Many2one('product.product', string='Paid Amount Product',
                                          domain=[('available_in_pos', '=', True)])
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
