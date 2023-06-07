odoo.define('pos_custome.Models', function (require) {
  'use strict';

  const Registries = require('point_of_sale.Registries');
  const { PosGlobalState } = require('point_of_sale.models');
  var field_utils = require('web.field_utils');
  var utils = require('web.utils');
  var new_currency = [];
  var complementary_currency;
  var round_di = utils.round_decimals;
  
  const NewPosGlobalState = (PosGlobalState) => class NewPosGlobalState extends PosGlobalState { 
      async load_server_data() {
          const loadedData = await this.env.services.rpc({
              model: 'pos.session',
              method: 'load_pos_data',
              args: [[odoo.pos_session_id]],
          });
          new_currency = await this.env.services.rpc({
              model: 'res.currency',
              method: 'search_read',
              // fields: ['name', 'symbol', 'position'],
              // domain: [['full_name', 'in', names]],
          });
          console.log("loadedData", loadedData);
          console.log("new_currency", new_currency);
          
          // Get the complementary_currency field from pos.config
          complementary_currency = await this.env.services.rpc({
              model: 'pos.config',
              method: 'search_read',
              fields: ['complementary_currency'],
              domain: [['id', '=', odoo.pos_session_id]],
          });
          console.log("complementary_currency", complementary_currency);
          
          await this._processData(loadedData);
          return this.after_load_server_data();
      }
      
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
          const defaultCashDetailsCurrency = closingData.default_cash_details_currency;
          const otherPaymentMethods = closingData.other_payment_methods;
          const isManager = closingData.is_manager;
          const amountAuthorizedDiff = closingData.amount_authorized_diff;
          const cashControl = this.config.cash_control;

          // Component state and refs definition
          const state = { notes: '', acceptClosing: false, payments: {} };
          
          if (cashControl) {
              state.payments[defaultCashDetails.id] = { counted: 0, difference: -defaultCashDetails.amount, number: 0 };
              state.payments[defaultCashDetailsCurrency.id] = { counted: 0, difference: -defaultCashDetailsCurrency.amount, number: 0 };
          }
          
          if (otherPaymentMethods.length > 0) {
              otherPaymentMethods.forEach(pm => {
                  if (pm.type === 'bank') {
                      state.payments[pm.id] = { counted: this.round_decimals_currency(pm.amount), difference: 0, number: pm.number };
                  }
              });
          }
          
          return {
              ordersDetails, paymentsAmount, payLaterAmount, openingNotes, defaultCashDetails,defaultCashDetailsCurrency, otherPaymentMethods,
              isManager, amountAuthorizedDiff, state, cashControl
          };
      }

      get_currency_rate() {
          // if (this.env.pos.get_order().pricelist.display_name == this.default_pricelist.display_name) {
          //     return 1;
          // }
          // else {
          //     var new_currency2 = new_currency.filter(o => o.full_name === this.env.pos.get_order().pricelist.name);
          //     return new_currency2[0].rate;
          // }
          
          // Get the complementary_currency field from pos.config
          // var complementary            //currency = this.env.pos.config.complementary_currency;
            //search in res.currency model if complementary_currency exists and grab the rate
            var complementary_currency_rate = new_currency.find(o => o.name === complementary_currency);
            return complementary_currency_rate.rate;
        }

        // format_currency_no_symbol2(amount, precision, currency) {
        //     if (!currency) {
        //         currency = this.currency
        //     }
        //     var decimals = currency[0].decimal_places;

        //     if (precision && this.dp[precision] !== undefined) {
        //         decimals = this.dp[precision];
        //     }

        //     if (typeof amount === 'number') {
        //         amount = round_di(amount, decimals).toFixed(decimals);
        //         amount = field_utils.format.float(round_di(amount, decimals), {
        //             digits: [69, decimals],
        //         });
        //     }
        //     return amount;
        // }
    };

    Registries.Model.extend(PosGlobalState, NewPosGlobalState);
});

