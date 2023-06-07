from odoo import fields, models, api

class PosSessionInheit(models.Model):
    _inherit = 'pos.session'


    def get_closing_control_data(self):
        self.ensure_one()
        orders = self.order_ids.filtered(lambda o: o.state == 'paid' or o.state == 'invoiced')
        payments = orders.payment_ids.filtered(lambda p: p.payment_method_id.type != "pay_later")
        pay_later_payments = orders.payment_ids - payments
        cash_payment_method_ids = self.payment_method_ids.filtered(lambda pm: pm.type == 'cash')
        default_cash_payment_method_id = cash_payment_method_ids[0] if cash_payment_method_ids else None
        total_default_cash_payment_amount = sum(payments.filtered(lambda p: p.payment_method_id == default_cash_payment_method_id).mapped('amount')) if default_cash_payment_method_id else 0
        other_payment_method_ids = self.payment_method_ids - default_cash_payment_method_id if default_cash_payment_method_id else self.payment_method_ids
        cash_in_count = 0
        cash_out_count = 0
        cash_in_out_list = []
        last_session = self.search([('config_id', '=', self.config_id.id), ('id', '!=', self.id)], limit=1)
        for cash_move in self.statement_line_ids.sorted('create_date'):
            if cash_move.amount > 0:
                cash_in_count += 1
                name = f'Cash in {cash_in_count}'
            else:
                cash_out_count += 1
                name = f'Cash out {cash_out_count}'
            cash_in_out_list.append({
                'name': cash_move.payment_ref if cash_move.payment_ref else name,
                'amount': cash_move.amount
            })

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
                          + sum(self.statement_line_ids.mapped('amount')),
                'opening': last_session.cash_register_balance_end_real,
                'payment_amount': total_default_cash_payment_amount,
                'moves': cash_in_out_list,
                'id': default_cash_payment_method_id.id
            } if default_cash_payment_method_id else None,
            'default_cash_details_currency': {
                'name': default_cash_payment_method_id.name,
                'amount': last_session.cash_register_balance_end_real
                          + total_default_cash_payment_amount
                          + sum(self.statement_line_ids.mapped('amount')),
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
