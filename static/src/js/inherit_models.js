odoo.define('pos_custome.models', function (require) {
  "use strict";

  const { PosGlobalState } = require('point_of_sale.models');
  const Registries = require('point_of_sale.Registries');

  const NewPosGlobalState = class extends PosGlobalState {
    async getClosePosInfo() {
      const closingData = await this.env.services.rpc({
        model: 'pos.session',
        method: 'get_closing_control_data',
        args: [[this.pos_session.id]]
      });
      const ordersDetails = closingData.orders_details;
      const paymentsAmount = closingData.payments_amount;
      const payLaterAmount = closingData.pay_later_amount;
      const openingNotes = closingData.opening_notes;
      const defaultCashDetails = closingData.default_cash_details;
      const otherPaymentMethods = closingData.other_payment_methods;
      const isManager = closingData.is_manager;
      const amountAuthorizedDiff = closingData.amount_authorized_diff;
      const cashControl = this.config.cash_control;

      // component state and refs definition
      const state = { notes: '', acceptClosing: false, payments: {} };
      if (cashControl) {
        state.payments[defaultCashDetails.id] = { counted: 0, difference: -defaultCashDetails.amount, number: 0 };
      }
      if (otherPaymentMethods.length > 0) {
        otherPaymentMethods.forEach(pm => {
          if (pm.type === 'bank') {
            state.payments[pm.id] = { counted: this.round_decimals_currency(pm.amount), difference: 0, number: pm.number };
          }
        });
      }
      return {
        ordersDetails, paymentsAmount, payLaterAmount, openingNotes, defaultCashDetails, otherPaymentMethods,
        isManager, amountAuthorizedDiff, state, cashControl
      };
    }
  };

  Registries.Model.extend('pos_global_state', NewPosGlobalState);

  return NewPosGlobalState;
});
