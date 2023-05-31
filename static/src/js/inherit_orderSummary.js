odoo.define('custom_module.OrderSummary', function(require) {
    'use strict';

    const OrderSummary = require('point_of_sale.OrderSummary');
    const Registries = require('point_of_sale.Registries');
    const { float_is_zero } = require('web.utils');
    

    const CustomOrderSummary = OrderSummary  => class extends OrderSummary{
        // ...votre code personnalisé ici... 
        format_currency_amount(amount){
            const pre = this.env.pos.config.complementary_currency_position === 'before';
            console.log("=======++++++=====",pre,"=====+++++=======")
            const symbol = this.env.pos.config.complementary_currency_symbol || '';
            console.log("=======++++++=====",symbol,"=====+++++=======")
            return (pre ? symbol : '') + amount + (pre ? '' : symbol);
        }
        getTotaldevise() {
            const taux = this.env.pos.config.taux;
            const total = this.props.order.get_total_with_tax() * taux;
            return this.format_currency_amount(total);
        }       
        getTaxdevise(){
            const taux = this.env.pos.config.taux;
            const total = this.props.order.get_total_with_tax() * taux;
            const totalWithoutTax = this.props.order.get_total_without_tax() * taux;
            const taxAmount = total - totalWithoutTax;
            return {
                hasTax: !float_is_zero(this.format_currency_amount(taxAmount), this.env.pos.currency.decimal_places),
                displayAmount: this.format_currency_amount(taxAmount),
            };
        }
        // getCurrency(){
        //     const currency = this.env.pos.pos_complementary_currency
        //     console.log("============++++++++=========",currency,"===========+++++=====")
        // }
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

    Registries.Component.extend(OrderSummary, CustomOrderSummary);  // Enregistrement de la classe étendue

    return CustomOrderSummary;
});

