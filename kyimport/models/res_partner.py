# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'
    _order = 'name'

    phone2 = fields.Char("Téléphone 2")
    fax = fields.Char("Fax")
    siret = fields.Char("Siret")
    #import_sap_listprice_id = fields.Integer("SAP listprice id")
    payment_term_id_use_in_filter = fields.Char(string='Payment term', related='property_payment_term_id.name', readonly=True, store=True)

    @api.model
    def create_from_ui(self, partner):
        """override function from point_of_sale from vendor point of view"""

        partner_id = partner.pop('id', False)
        if partner_id:
            pass
        else:
            partner['user_id'] = self.env.user.id # vendor id
            partner['is_company'] = True # all customer create by vendor is a company

        partner_id = super(ResPartner, self).create_from_ui(partner)
        return partner_id

