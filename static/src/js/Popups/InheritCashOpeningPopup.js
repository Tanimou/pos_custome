odoo.define('pos_custome.InheritCashOpeningPopup', function (require) {
    'use strict';

    const CashOpeningPopup = require('point_of_sale.CashOpeningPopup');
    const Registries = require('point_of_sale.Registries');
    const { useState } = owl;

    const InheritCashOpeningPopup = (CashOpeningPopup) =>
        class extends CashOpeningPopup {
            setup() {
                super.setup();
                this.manualInputCashCount = null;
                this.state = useState({
                    notes: "",
                    openingCash: this.env.pos.pos_session.cash_register_balance_start || 0,
                    openingCashCurrency: this.env.pos.pos_session.cash_register_balance_start_currency|| 0,
                    displayMoneyDetailsPopup: false,
                });
            }
            async confirm() {  
                this.env.pos.pos_session.cash_register_balance_start = this.state.openingCash;
                this.env.pos.pos_session.cash_register_balance_start_currency = this.state.openingCashCurrency;
                this.env.pos.pos_session.state = 'opened';
                this.rpc({ 
                       model: 'pos.session',
                        method: 'set_cashbox_pos',
                        args: [this.env.pos.pos_session.id, this.state.openingCash, this.state.notes,this.state.openingCashCurrency],
                });
                super.confirm();
            }
            openDetailsPopup() {
                this.state.openingCash = 0;
                this.state.openingCashCurrency = 0;
                this.state.notes = "";
                this.state.displayMoneyDetailsPopup = true;
            }
            updateCashOpening({ total,totalcurrency, moneyDetailsNotes }) {
                this.state.openingCash = total;
                this.state.openingCashCurrency = totalcurrency;
                if (moneyDetailsNotes) {
                    this.state.notes = moneyDetailsNotes;
                }
                this.manualInputCashCount = false;
                this.closeDetailsPopup();
            }
            handleInputChange() {
                this.manualInputCashCount = true;
                this.state.notes = "";
                if (typeof(this.state.openingCash) !== "number") {
                    this.state.openingCash = 0;
                    this.state.openingCashCurrency = 0;
                }
            }
            get_related_currency_name(){
                const pos_complementary_currency = this.env.pos.config.complementary_currency
    
                if (pos_complementary_currency[1]){
                    console.log("=========",pos_complementary_currency,"=============");
                    return pos_complementary_currency[1];
                }
               else{
                    return ' ';
               }
                
            }
        };
    Registries.Component.extend(CashOpeningPopup, InheritCashOpeningPopup);

    return InheritCashOpeningPopup;
});