# -*- coding: utf-8 -*-

from odoo import models, api, fields, _

class ReportAccountAgedPartner(models.AbstractModel):
    _name = "sales_trip.aged.partner"
    _description = "Aged Partner Balances for Trip Report"
    _inherit = 'account.aged.partner'

    def _format_line(self, value_dict, value_getters, value_formatters, current, options, total=False):
        """Add new param from parent method _format_line
        :param property_payment_term_id: partner payment term id
        :return dict: the report line
        """
        res = super(ReportAccountAgedPartner, self)._format_line(value_dict, value_getters, value_formatters, current, options, total)
        id = value_dict['partner_id'][0]
        browsed_partner = self.env['res.partner'].browse(id)
        res['property_payment_term_id'] = browsed_partner.property_payment_term_id.id

        return res
