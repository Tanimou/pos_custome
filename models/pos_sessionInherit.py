# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from datetime import timedelta
from itertools import groupby
import json
from odoo import api, fields, models, _, Command
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare
from odoo.osv.expression import AND, OR
from odoo.service.common import exp_version


class PosSessionInherit(models.Model):
    _inherit="pos.session"
    
    cash_in_out_list = fields.Char(string='Cash In/Out List')
    
    def get_closing_control_data(self):
        if not self.env.user.has_group('point_of_sale.group_pos_user'):
            raise AccessError(_("You don't have the access rights to get the point of sale closing control data."))
        self.ensure_one()
        orders = self.order_ids.filtered(lambda o: o.state in ['paid', 'invoiced'])
        payments = orders.payment_ids.filtered(lambda p: p.payment_method_id.type != "pay_later")
        pay_later_payments = orders.payment_ids - payments
        cash_payment_method_ids = self.payment_method_ids.filtered(lambda pm: pm.type == 'cash')
        default_cash_payment_method_id = cash_payment_method_ids[0] if cash_payment_method_ids else None
        total_default_cash_payment_amount = sum(payments.filtered(lambda p: p.payment_method_id == default_cash_payment_method_id).mapped('amount')) if default_cash_payment_method_id else 0
        other_payment_method_ids = self.payment_method_ids - default_cash_payment_method_id if default_cash_payment_method_id else self.payment_method_ids
        cash_in_count = 0
        cash_out_count = 0
        cash_symbol = self.currency_id.symbol or self.currency_id.name
        cash_in_out_list = []
        last_session = self.search([('config_id', '=', self.config_id.id), ('id', '!=', self.id)], limit=1)
        if self.cash_in_out_list:
            cash_in_out_list = json.loads(self.cash_in_out_list)
        # for cash_move in self.sudo().statement_line_ids.sorted('create_date'):
        #     if cash_move.amount > 0:
        #         cash_in_count += 1
        #         name = f'Cash in {cash_in_count}'
        #     else:
        #         cash_out_count += 1
        #         name = f'Cash out {cash_out_count}'
        #     cash_in_out_list.append({
        #         'name': cash_move.payment_ref or name,
        #         'amount': cash_move.amount,
        #         'is_new_currency_selected':cash_move.is_new_currency_selected,
        #     })
        last_cash_move = self.sudo().statement_line_ids.sorted('create_date')[-1]
        if last_cash_move.amount > 0:
            cash_in_count = len([move for move in cash_in_out_list if move['amount'] > 0]) + 1
            name = f'Cash in {cash_in_count}'
        else:
            cash_out_count = len([move for move in cash_in_out_list if move['amount'] < 0]) + 1
            name = f'Cash out {cash_out_count}'

        cash_in_out_list.append({
            'name': last_cash_move.payment_ref or name,
            'amount': last_cash_move.amount,
            'is_new_currency_selected': last_cash_move.is_new_currency_selected,
        })

        self.cash_in_out_list = json.dumps(cash_in_out_list)
        print("cash_in_out_list ",cash_in_out_list)
        print("is complementary currency ",self.config_id.complementary_currency)
        print("is complementary currency symbol ",self.config_id.complementary_currency_symbol)
        print("is complementary currency active ",self.config_id.is_complementary_currency_active)
        # print("statement line ids ",self.sudo().statement_line_ids)
        return {
            'orders_details': {
                'quantity': len(orders),
                'amount': sum(orders.mapped('amount_total'))
            },
            'payments_amount': sum(payments.mapped('amount')),
            'pay_later_amount': sum(pay_later_payments.mapped('amount')),
            'opening_notes': self.opening_notes,
            'default_cash_details': {
                'name': default_cash_payment_method_id.name,
                'amount': last_session.cash_register_balance_end_real
                          + total_default_cash_payment_amount
                          + sum(self.sudo().statement_line_ids.mapped('amount')),
                'opening': last_session.cash_register_balance_end_real,
                'payment_amount': total_default_cash_payment_amount,
                'moves': cash_in_out_list,
                'id': default_cash_payment_method_id.id
            } if default_cash_payment_method_id else None,
            'other_payment_methods': [{
                'name': pm.name,
                'amount': sum(orders.payment_ids.filtered(lambda p: p.payment_method_id == pm).mapped('amount')),
                'number': len(orders.payment_ids.filtered(lambda p: p.payment_method_id == pm)),
                'id': pm.id,
                'type': pm.type,
            } for pm in other_payment_method_ids],
            'is_manager': self.user_has_groups("point_of_sale.group_pos_manager"),
            'amount_authorized_diff': self.config_id.amount_authorized_diff if self.config_id.set_maximum_difference else None
        }
        
    #write a function to get this.state.isNewCurrencySelected coming from js file
    #this.state.isNewCurrencySelected is located at inherit_CashMovePopup.js file
    
    # def _check_is_new_currency_selected(self):
    #     #read the inherit_CashMovePopup.js file
    #     #this.state.isNewCurrencySelected is located at inherit_CashMovePopup.js file
        
    #     informations=
        