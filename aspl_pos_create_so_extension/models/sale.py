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
from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    amount_due = fields.Float("Amount Due")

    @api.model
    def get_sale_order_data(self, user):
        if user['display_own_sales_order']:
            # query = """SELECT id,name,date_order,partner_id,l10n_in_gst_treatment,partner_invoice_id,
            #            partner_shipping_id,amount_due,note,user_id,amount_total,state FROM sale_order
            #            where user_id = %s""" % (user['id'])
            query = """SELECT id,name,date_order,partner_id,partner_invoice_id,
                           partner_shipping_id,amount_due,note,user_id,amount_total,state FROM sale_order
                           where user_id = %s""" % (user['id'])
        else:
            # query = """SELECT id,name,date_order,partner_id,l10n_in_gst_treatment,partner_invoice_id,
            #            partner_shipping_id,amount_due,note,user_id,amount_total,state FROM sale_order """
            query = """SELECT id,name,date_order,partner_id,partner_invoice_id,
                           partner_shipping_id,amount_due,note,user_id,amount_total,state FROM sale_order """
        self.env.cr.execute(query)
        return [self.env.cr.dictfetchall(), self.get_invoice_data()]

    @api.model
    def get_invoice_data(self):
        query = """SELECT * FROM account_move WHERE move_type = 'out_invoice' """
        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()


    @api.model
    def get_return_product(self, sale_order_id):
        picking_obj = self.env['stock.picking']
        product_list = []
        if sale_order_id:
            picking_id = picking_obj.search([('sale_id', '=', sale_order_id),
                                             ('state', '=', 'done'),
                                             ('picking_type_id.code', '=', 'outgoing')])
            for out in picking_id:
                for out_move in out.move_lines:
                    product_list.append({
                        'product_id': out_move.product_id.id,
                        'qty': out_move.quantity_done,
                        'p_name': out_move.product_id.name,
                        'sale_order_id': sale_order_id,
                        'id': out_move.id,
                        'return_qty': 0,
                    })
                for product in product_list:
                    in_picking_id = picking_obj.search([('origin', '=', out.name),
                                                        ('state', '!=', 'cancel'),
                                                        ('picking_type_id.code', '=', 'incoming')])
                    for receipt in in_picking_id:
                        if receipt.origin == out.name:
                            for move in receipt.move_lines:
                                if move.product_id.id == product.get('product_id'):
                                    product.update({'qty': product.get('qty') - move.product_uom_qty})
        return product_list


    @api.model
    def return_sale_order(self, lines):
        order_id = int(lines[0].get('sale_order_id'))
        picking_obj = self.env['stock.picking']
        picking_id = picking_obj.search([('sale_id', '=', order_id),
                                         ('state', '=', 'done'), ('picking_type_id.code', '=', 'outgoing')])
        new_picking = False
        for pick in picking_id:
            picking_type_id = pick.picking_type_id.return_picking_type_id.id or pick.picking_type_id.id
            new_picking = picking_obj.create({
                'move_lines': [],
                'picking_type_id': picking_type_id,
                'state': 'draft',
                'origin': pick.name,
                'location_id': pick.location_dest_id.id,
                'location_dest_id': pick.move_lines[0].location_id.id,
                'partner_id': self.env['sale.order'].browse(order_id).partner_id.id,
            })
            move_list = []
            for line in lines:
                move_id = self.env['stock.move'].search([('product_id', '=', line.get('product_id')),
                                                         ('picking_id', '=', pick.id), ('state', '=', 'done')])
                return_move_id = {
                    'product_id': line.get('product_id'),
                    'product_uom_qty': abs(float(line.get('return_qty'))),
                    'state': 'draft',
                    'location_id': move_id.location_dest_id.id,
                    'location_dest_id': move_id.location_id.id,
                    'warehouse_id': pick.picking_type_id.warehouse_id.id,
                    'origin_returned_move_id': move_id.id,
                    'procure_method': 'make_to_stock',
                    'picking_id': new_picking.id,
                    'product_uom': move_id.product_uom.id,
                    'name': new_picking.name,
                }
                move_list.append((0, 0, return_move_id))
            new_picking.update({'move_lines': move_list})
        new_picking.action_confirm()
        new_picking.action_assign()
        wizard = self.env['stock.immediate.transfer'].with_context(
            dict(self.env.context, default_show_transfers=False,
                 default_pick_ids=[(4, new_picking.id)])).create({})
        wizard.process()
        new_picking.button_validate()
        new_picking.write({
            'sale_id': order_id,
        })
        return new_picking.id


    @api.model
    def pay_from_so_screen(self, vals):
        if vals.get("sale_order_id"):
            sale_id = self.browse(vals.get("sale_order_id"))
            payment_lines = vals.get("paymentlines")
            for invoice_id in sale_id.invoice_ids:
                for journal in payment_lines:
                    pos_payment_method = self.env['pos.payment.method'].browse(journal.get('journal_id'))
                    account_journal = self.env['account.journal'].search(
                        [('type', 'ilike', pos_payment_method.name)],
                        limit=1)
                    register_payments = self.env['account.payment.register'].with_context(
                        active_model='account.move', active_ids=invoice_id.ids).create({
                        'journal_id': account_journal.id, 'amount': journal.get('amount')
                    })
                    register_payments._create_payments()
                created_invoice = {
                    'id': invoice_id.id,
                    'name': invoice_id.name,
                    'partner_id': invoice_id.partner_id[0].id,
                    'date': invoice_id.date,
                    'invoice_date_due': invoice_id.invoice_date_due,
                    'amount_residual': invoice_id.amount_residual,
                    'amount_total': invoice_id.amount_total,
                }
                sale_id.write({'amount_due': invoice_id.amount_residual})
                sale_order_data = {
                    'id': sale_id.id,
                    'name': sale_id.name,
                    'amount_due': sale_id.amount_due,
                }
                if created_invoice:
                    return created_invoice, sale_order_data
                return sale_order_data


    @api.model
    def pay_invoice(self, vals):
        invoice_id = vals.get("invoice_id")
        invoice = self.env['account.move'].browse(invoice_id)
        sale_order = self.search([('name', '=', invoice.invoice_origin)])
        if invoice.state == "draft":
            invoice.action_post()
        payment_lines = vals.get("paymentlines")
        for journal in payment_lines:
            pos_payment_method = self.env['pos.payment.method'].browse(journal.get('journal_id'))
            account_journal = self.env['account.journal'].search(
                [('type', 'ilike', pos_payment_method.name)],
                limit=1)
            register_payments = self.env['account.payment.register'].with_context(
                active_model='account.move', active_ids=invoice_id).create(
                {'journal_id': account_journal.id, 'amount': journal.get('amount')})
            register_payments._create_payments()
        invoice_val = {
            'id': invoice.id,
            'name': invoice.name,
            'partner_id': invoice.partner_id[0].id,
            'date': invoice.date,
            'state': invoice.state,
            'invoice_date_due': invoice.invoice_date_due,
            'amount_residual': invoice.amount_residual,
            'amount_total': invoice.amount_total,
        }
        sale_order.write({'amount_due': invoice.amount_residual})
        sale_val = {
            'id': sale_order.id,
            'amount_due': sale_order.amount_due
        }
        return invoice_val, sale_val


    @api.model
    def get_sale_order_val(self, sale_id):
        sale_order_data = {
            'name': sale_id.name,
            'amount_due': sale_id.amount_due,
            'amount_total': sale_id.amount_total,
            'date_order': sale_id.date_order,
            'signature': sale_id.signature,
            'id': sale_id.id,
            # 'l10n_in_gst_treatment': sale_id.l10n_in_gst_treatment,
            'note': sale_id.note,
            'state': sale_id.state,
            'user_id': sale_id.user_id,
            'partner_id': sale_id.partner_id[0].id,
            'partner_invoice_id': sale_id.partner_invoice_id.id,
            'partner_shipping_id': sale_id.partner_shipping_id.id,
        }
        return sale_order_data


    @api.model
    def create_sale_order_line(self, order_line, sale_id):
        product_obj = self.env['product.product']
        sale_order_line_obj = self.env['sale.order.line']
        sale_line = {'order_id': sale_id.id}
        for line in order_line:
            prod_rec = product_obj.browse(line['product_id'])
            prod_desc = prod_rec.name_get()[0][1]
            if prod_rec.description_sale:
                prod_desc += '\n' + prod_rec.description_sale
            sale_line.update({
                'name': prod_desc or '',
                'product_id': prod_rec.id,
                'product_uom_qty': line['qty'],
                'discount': line.get('discount'),
                'price_unit': line.get('price_unit'),
            })
            new_product = sale_order_line_obj.new({'product_id': prod_rec.id})
            prod = new_product.product_id_change()
            sale_line.update(prod)
            sale_line.update({'price_unit': line['price_unit']})
            taxes = map(lambda a: a.id, prod_rec.taxes_id)
            if taxes:
                sale_line.update({'tax_id': [(6, 0, taxes)]})
            sale_line.update({'product_uom': prod_rec.uom_id.id})
            sale_order_line_obj.create(sale_line)


    @api.model
    def create_sales_order(self, vals):
        sale_order_obj = self.env['sale.order']
        customer_id = vals.get('customer_id')
        orderline = vals.get('orderlines')
        journal = vals.get('journal')
        sale_id = False
        if not vals.get('sale_order_id'):
            partner_records = self.get_res_partner_record(customer_id)
            payment_term_id = None
            if partner_records is not None:
                for partner_record in partner_records:
                    payment_term_id = partner_record.property_payment_term_id.id

            sale = {
                'partner_id': customer_id,
                'date_order': vals.get('orderDate'),
                'partner_shipping_id': int(vals.get('partner_shipping_id')),
                'partner_invoice_id': int(vals.get('partner_invoice_id')),
                'note': vals.get('note') and vals.get('note') or '',
                'signature': vals.get('sign') and vals.get('sign') or None,
                'signed_by': vals.get('signed_by') and vals.get('signed_by') or None,
                'signed_on': vals.get('signed_on') and vals.get('signed_on') or None,
                'payment_term_id': payment_term_id,
                'workflow_process_id': 1,
            }
            # if vals.get('gstTreatment'):
            #     sale.update({'l10n_in_gst_treatment': vals.get('gstTreatment')})
            new = sale_order_obj.new({'partner_id': customer_id})
            new.onchange_partner_id()
            sale_id = sale_order_obj.create(sale)
            self.create_sale_order_line(orderline, sale_id)
            if vals.get('operation') == 'confirm':
                sale_id.action_confirm()
            if vals.get('operation') == 'direct_pay':
                sale_id.action_confirm()
                location_id = self.env['stock.picking.type'].browse(vals.get('location_id'))
                if sale_id:
                    for picking_id in sale_id.picking_ids.filtered(lambda d: d.state not in ('done', 'cancel')):
                        if location_id.default_location_src_id:
                            picking_id.move_lines.write({'location_id': location_id.id})
                            picking_id.action_confirm()
                            picking_id.action_assign()
                            wizard = self.env['stock.immediate.transfer'].with_context(
                                dict(self.env.context, default_show_transfers=False,
                                     default_pick_ids=[(4, picking_id.id)])).create({})
                            wizard.process()
                            picking_id.button_validate()
                    sale_id._create_invoices()
                    created_invoice = False
                    for invoice_id in sale_id.invoice_ids.filtered(lambda d: d.state not in ('posted', 'cancel')):
                        invoice_id.action_post()
                        for journal in journal:
                            pos_payment_method = self.env['pos.payment.method'].browse(journal.get('journal_id'))
                            account_journal = self.env['account.journal'].search(
                                [('type', 'ilike', pos_payment_method.name)],
                                limit=1)
                            register_payments = self.env['account.payment.register'].with_context(
                                active_model='account.move', active_ids=invoice_id.ids).create(
                                {'journal_id': account_journal.id, 'amount': journal.get('amount')})
                            register_payments._create_payments()
                        created_invoice = {
                            'id': invoice_id.id,
                            'name': invoice_id.name,
                            'partner_id': invoice_id.partner_id[0].id,
                            'date': invoice_id.date,
                            'invoice_date_due': invoice_id.invoice_date_due,
                            'amount_residual': invoice_id.amount_residual,
                            'amount_total': invoice_id.amount_total,
                        }
                        sale_id.write({'amount_due': invoice_id.amount_residual})
                    sale_order_data = self.get_sale_order_val(sale_id)
                    if created_invoice and sale_order_data:
                        return sale_order_data, created_invoice
                    else:
                        return sale_order_data
        elif vals.get('sale_order_id'):
            if customer_id:
                sale_id = self.browse(vals.get('sale_order_id'))

                partner_records = self.get_res_partner_record(customer_id)
                payment_term_id = None
                if partner_records is not None:
                    for partner_record in partner_records:
                        payment_term_id = partner_record.property_payment_term_id.id

                if sale_id:
                    sale = {
                        'partner_id': int(customer_id),
                        'partner_invoice_id': int(vals.get('partner_invoice_id')),
                        'partner_shipping_id': int(vals.get('partner_shipping_id')),
                        'date_order': vals.get('orderDate'),
                        'note': vals.get('note') or '',
                        'signature': vals.get('sign') and vals.get('sign') or None,
                        'signed_by': vals.get('signed_by') and vals.get('signed_by') or None,
                        'signed_on': vals.get('signed_on') and vals.get('signed_on') or None,
                        'payment_term_id': payment_term_id,
                        'workflow_process_id': 1,
                    }
                    # if vals.get('gstTreatment'):
                    #     sale.update({'l10n_in_gst_treatment': vals.get('gstTreatment')})
                    sale_id.write(sale)
                    [line.sudo().unlink() for line in sale_id.order_line]
                    self.create_sale_order_line(orderline, sale_id)
                    if vals.get('operation') == 'confirm':
                        sale_id.action_confirm()
        return [self.get_sale_order_val(sale_id)]


    @api.model
    def get_res_partner_record(self, id):
        """Retourne l'enregistrement associé à l'id client"""

        records = None

        records = self.env['res.partner'].search([['id', '=', id]])

        return records
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
