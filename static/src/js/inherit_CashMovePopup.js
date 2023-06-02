odoo.define('pos_custome.InheritCashMovePopup', function (require) {
    'use strict';

    const CashMovePopup = require('point_of_sale.CashMovePopup');
    const Registries = require('point_of_sale.Registries');
    const inherit_models= require('pos_custome.Models')
    const { useState } = owl;

    const InheritCashMovePopup = (CashMovePopup) =>
        class extends CashMovePopup {
            setup() {
                super.setup();
                this.state = useState({
                    inputComment: '',
                    inputType: '', // '' | 'in' | 'out'
                    inputAmount: '',
                    inputReason: '',
                    inputCurrency: this.env.pos.get_order().pos.currency.name,
                    inputHasError: false,
                });
            }

             active_currency() {
                 console.log("compleme,tary_currency", this.env.pos)
                 return [{ 'name': this.env.pos.get_order().pos.currency.name },{ 'name': this.env.pos.config.complementary_currency[1] }];
            }
                
            confirm() {
                if ((this.state.inputComment.trim() == '') && (this.state.inputReason.trim() == 'Autres')) {
                    this.state.inputHasError = true;
                    this.errorMessage = this.env._t('Veuillez mettre une description svp !');
                    return;
                }
                return super.confirm();
            }

            onClickButton(type) {
                let amount = this.state.inputAmount;
                if (type === 'in') {
                    this.state.inputAmount = amount.charAt(0) === '-' ? amount.substring(1) : amount;
                } else {
                    this.state.inputAmount = amount.charAt(0) === '-' ? amount : `-${amount}`;
                }
                this.state.inputType = type;
                this.state.inputHasError = false;
                this.inputAmountRef.el && this.inputAmountRef.el.focus();
            }
            
            getPayload() {
                let data = super.getPayload()
                data.comment = this.state.inputComment.trim();

                console.log('data ....in data .', data);
                return data;
            }
        };
    Registries.Component.extend(CashMovePopup, InheritCashMovePopup);

    return InheritCashMovePopup;
});