odoo.define('pos_custome.InheritCashOpeningPopup', function (require) {
    'use strict';

    const CashOpeningPopup = require('point_of_sale.CashOpeningPopup');
    const Registries = require('point_of_sale.Registries');
    const { useState } = owl;

    const InheritOpeningPopup = (CashOpeningPopup) =>
        class extends CashOpeningPopup {
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
    Registries.Component.extend(CashOpeningPopup, InheritOpeningPopup);

    return InheritCashMovePopup;
});