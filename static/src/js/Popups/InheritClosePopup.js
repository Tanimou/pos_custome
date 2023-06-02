odoo.define('pos_custome.InheritClosePopup', function (require) {
    'use strict';

    const ClosePosPopup = require('point_of_sale.ClosePosPopup');
    const Registries = require('point_of_sale.Registries');
    const { useState } = owl;

    const InheritClosePopup = (ClosePosPopup) =>
        class extends ClosePosPopup {
            format_currency_amount(amount){
                const pre = this.env.pos.config.complementary_currency_position === 'before';
                console.log("=======++++++=====",pre,"=====+++++=======")
                const symbol = this.env.pos.config.complementary_currency_symbol || '';
                console.log("=======++++++=====",symbol,"=====+++++=======")
                return (pre ? symbol : '') + amount + (pre ? '' : symbol);
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
    Registries.Component.extend(ClosePosPopup, InheritClosePopup);

    return InheritClosePopup;
});