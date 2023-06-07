from odoo import fields, models, api

class PosSessionInherit(models.Model):
    _inherit = 'pos.session'
    cash_register_balance_end_real_currency = fields.Monetary(
        string="Ending Balance",
        readonly=True)
    cash_register_balance_start_currency = fields.Monetary(
        string="Starting Balance",
        readonly=True)
    cash_register_total_entry_encoding_currency = fields.Monetary(
        compute='_compute_cash_balance_currency',
        string='Total Cash Transaction',
        readonly=True)
    cash_register_balance_end_real_currency = fields.Monetary(
        compute='_compute_cash_balance_currency',
        string="Theoretical Closing Balance",
        help="Opening balance summed to all cash transactions.",
        readonly=True)
    cash_register_difference_currency = fields.Monetary(
        compute='_compute_cash_balance_currency',
        string='Before Closing Difference',
        help="Difference between the theoretical closing balance and the real closing balance.",
        readonly=True)
    cash_real_transaction_currency = fields.Monetary(string='Transaction', readonly=True)
    cash_register_balance_end_currency = fields.Monetary(
        compute='_compute_cash_balance_currency',
        string="Theoretical Closing Balance",
        help="Opening balance summed to all cash transactions.",
        readonly=True)
    
    @api.depends('payment_method_ids', 'order_ids', 'cash_register_balance_start_currency')
    def _compute_cash_balance_currency(self):
        for session in self:
            cash_payment_method = session.payment_method_ids.filtered('is_cash_count')[:1]
            if cash_payment_method:
                total_cash_payment = 0.0
                last_session = session.search([('config_id', '=', session.config_id.id), ('id', '!=', session.id)], limit=1)
                result = self.env['pos.payment']._read_group([('session_id', '=', session.id), ('payment_method_id', '=', cash_payment_method.id)], ['amount'], ['session_id'])
                if result:
                    total_cash_payment = result[0]['amount']
                session.cash_register_total_entry_encoding = sum(session.statement_line_ids.mapped('amount')) + (
                    0.0 if session.state == 'closed' else total_cash_payment
                )
                session.cash_register_balance_end = last_session.cash_register_balance_end_real_currency + session.cash_register_total_entry_encoding_currency
                session.cash_register_difference = session.cash_register_balance_end_real_currency - session.cash_register_balance_end_currency
            else:
                session.cash_register_total_entry_encoding_currency = 0.0
                session.cash_register_balance_end_currency = 0.0
                session.cash_register_difference_currency = 0.0

    def action_pos_session_open(self):
            # we only open sessions that haven't already been opened
            for session in self.filtered(lambda session: session.state == 'opening_control'):
                values = {}
                if not session.start_at:
                    values['start_at'] = fields.Datetime.now()
                if session.config_id.cash_control and not session.rescue:
                    last_session = self.search([('config_id', '=', session.config_id.id), ('id', '!=', session.id)], limit=1)
                    session.cash_register_balance_start = last_session.cash_register_balance_end_real  # defaults to 0 if lastsession is empty
                    session.cash_register_balance_start_currency = last_session.cash_register_balance_end_real_currency  # defaults to 0 if lastsession is empty

                else:
                    values['state'] = 'opened'
                session.write(values)
            return True
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
                'amount': last_session.cash_register_balance_end_real_currency
                          + total_default_cash_payment_amount
                          + sum(self.statement_line_ids.mapped('amount')),
                'openingcurrency': 10,
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
    @api.model
    def set_cashbox_pos(self, cashbox_value, notes, cashbox_value_currency):
        self.state = 'opened'
        self.opening_notes = notes
        difference = cashbox_value - self.cash_register_balance_start
        self.cash_register_balance_start = cashbox_value
        self.cash_register_balance_start_currency = cashbox_value_currency
        self._post_statement_difference(difference)
        self._post_cash_details_message('Opening', difference, notes) 

    def _loader_params_pos_session(self):
        return {
            'search_params': {
                'domain': [('id', '=', self.id)],
                'fields': [
                    'id', 'name', 'user_id', 'config_id', 'start_at', 'stop_at', 'sequence_number',
                    'payment_method_ids', 'state', 'update_stock_at_closing', 'cash_register_balance_start',
                    'cash_register_balance_start_currency'
                ],
            },
        }
