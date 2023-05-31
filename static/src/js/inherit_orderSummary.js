odoo.define('pos_custome.OrderSummary', function (require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const { OrderSummary } = require('point_of_sale.OrderSummary');
    var field_utils = require('web.field_utils');
    const { float_is_zero } = require('web.utils');

    const NewOrderSummary = (OrderSummary) => class NewOrderSummary extends OrderSummary {
        getTotal() {
            console.log("this total", this.props.order.get_total_with_tax())
            return this.env.pos.format_currency(this.props.order.get_total_with_tax());
        }
        getTotalExchange() {
            const new_total= this.props.order.get_total_with_tax()/this.props.order.get_currency_rate();
            return this.env.pos.format_currency(new_total);
        }
        
        getTax() {
            const total = this.props.order.get_total_with_tax();
            const totalWithoutTax = this.props.order.get_total_without_tax();
            const taxAmount = total - totalWithoutTax;
            return {
                hasTax: !float_is_zero(taxAmount, this.env.pos.currency.decimal_places),
                displayAmount: this.env.pos.format_currency(taxAmount),
            };
        }
    }

    NewOrderSummary.template = 'OrderSummaryInherit';

    Registries.Component.extend(OrderSummary, NewOrderSummary);
return NewOrderSummary

});