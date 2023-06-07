odoo.define('pos_custome.InheritCashMovePopup', function (require) {
    'use strict';

    const CashMovePopup = require('point_of_sale.CashMovePopup');
    const Registries = require('point_of_sale.Registries');
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
                    inputCurrency: 'XOF',
                    inputHasError: false,
                });
            }
            // reasonValues() {
            //     const values = [{ 'name': ' ', 'value': 1 }, { 'name': 'Avance sur salaire', 'value': 2 },
            //     { 'name': 'Taxi', 'value': 3 }, { 'name': 'Salaire', 'value': 4 },
            //     { 'name': 'CIE', 'value': 5 }, { 'name': 'SODECI', 'value': 6 },
            //         { 'name': 'Matériels de nettoyage', 'value': 7 }, { 'name': 'Matériels caisse', 'value': 8 }, { 'name': 'Autres', 'value': 9 }]
            //     // const active_currencies = inherit_models.new_currency
            //     // console.log("active_currencies", active_currencies)
            //                 return values
            // }
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