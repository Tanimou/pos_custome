// BEGIN: updated code
odoo.define('pos_custome.InheritCashMovePopup', function (require) {
    'use strict';

    const CashMovePopup = require('point_of_sale.CashMovePopup');
    const Registries = require('point_of_sale.Registries');
    const inherit_models= require('pos_custome.Models')
    const { useState, useEffect } = owl;

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
                    isNewCurrencySelected: false,
                });
            }

            // mounted() {
            //     useEffect(() => {
            //         const session = this.env.pos.get('pos_session');
            //         session.is_complementary_currency_active = this.env.pos.config.is_complementary_currency_active;
            //     }, [this.env.pos.config.is_complementary_currency_active]);
            // }

            active_currency() {
                console.log("compleme,tary_currency", this.env.pos)
                return [{ 'name': this.env.pos.get_order().pos.currency.name },{ 'name': this.env.pos.config.complementary_currency[1] }];
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

            async confirm() {
                console.log("isNewCurrencySelected", this.state.isNewCurrencySelected)
                console.log("this.env.pos.config.is_complementary_currency_active", this.env.pos.config.is_complementary_currency_active)
                if ((this.state.inputComment.trim() == '') && (this.state.inputReason.trim() == 'Autres')) {
                    this.state.inputHasError = true;
                    this.errorMessage = this.env._t('Veuillez mettre une description svp !');
                    
                    return;
                }
                if ((this.state.inputCurrency == this.env.pos.get_order().pos.currency.name)) {
                    this.state.isNewCurrencySelected = false;
                    await this.rpc({
                        model: 'pos.config',
                        method: 'update_complementary_currency_active',
                        args: [this.state.isNewCurrencySelected],
                    });
                } else {
                    this.state.isNewCurrencySelected = true;
                    await this.rpc({
                        model: 'pos.config',
                        method: 'update_complementary_currency_active',
                        args: [this.state.isNewCurrencySelected],
                    });
                }
            
                return super.confirm();
            }
        };
    Registries.Component.extend(CashMovePopup, InheritCashMovePopup);

    return InheritCashMovePopup;
});
// END: updated code
