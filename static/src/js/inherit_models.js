odoo.define('pos_custome.Models',function(require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const { PosGlobalState } = require('point_of_sale.models');
    var field_utils = require('web.field_utils');
    var utils = require('web.utils');
    var new_currency = []
    var complementary_currency
    var round_di = utils.round_decimals;
    const NewPosGlobalState = (PosGlobalState) => class NewPosGlobalState extends PosGlobalState
    { 
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

                })
                console.log("loadedData", loadedData)
                console.log("new_currency", new_currency);
                //get the complementary_currency field from pos.config
                complementary_currency = await this.env.services.rpc({
                    model: 'pos.config',
                    method: 'search_read',
                    fields: ['complementary_currency'],
                    domain: [['id', '=', odoo.pos_session_id]],
                })
                console.log("complementary_currency", complementary_currency);
                await this._processData(loadedData);
                return this.after_load_server_data();
                
        }
        // format_currency(amount, precision) {

        //     // console.log("this currency is", this.currency)
        //     //  console.log("this pricelists is", this.pricelists)
        //     //  console.log("this new currency",new_currency)

        //     // console.log("this default price list is", this.default_pricelist)

        //     if (this.env.pos.get_order().pricelist.display_name == this.default_pricelist.display_name) {
        //         amount = this.format_currency_no_symbol(amount, precision, this.currency);
        //         if (this.currency.position === 'after') {
        //             return amount + ' ' + (this.currency.symbol || '');
        //         } else {
        //             return (this.currency.symbol || '') + ' ' + amount;
        //         }
        //     }

        //     else {
        //         var new_currency2 = new_currency.filter(o => o.full_name === this.env.pos.get_order().pricelist.name);
        //         console.log("this new currency2 is", new_currency2)

        //         console.log("this amount is", amount)
        //         // search in res.currency with this.env.services.rpc
        //         amount /= new_currency2[0].rate;
        //         console.log("this NEW amount is", amount)
        //         console.log("this result symbol is", new_currency2[0].symbol)
        //         console.log("this result position is", new_currency2[0].position)
        //         console.log("Current Pricelist Name: ", this.env.pos.get_order().pricelist.name);


        //         amount = this.format_currency_no_symbol2(amount, precision, new_currency2);
        //         if (new_currency2[0].position === 'after') {
        //             return amount + ' ' + (new_currency2[0].symbol || '');
        //         } else {
        //             return (new_currency2[0].symbol || '') + ' ' + amount;
        //         }

        //         // console.log("this new currency is", new_currency)

        //         // search in res.currency model if the name of the pricelist exists and grap the symbol
        //         // var ew_currency = this.pricelists.find(o => o.name === this.env.pos.get_order().pricelist.name);

        //     }
        
        // }
        get_currency_rate() {
            // if (this.env.pos.get_order().pricelist.display_name == this.default_pricelist.display_name) {
            //     return 1;
            // }
            // else {
            //     var new_currency2 = new_currency.filter(o => o.full_name === this.env.pos.get_order().pricelist.name);
            //     return new_currency2[0].rate;
            // }
            //get the complementary_currency field from pos.config
            // var complementary_currency = this.env.pos.config.complementary_currency;
            //search in res.currency model if complementary_currency exists and grap the rate
            complementary_currency_rate = new_currency.find(o => o.name === complementary_currency);
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
        
    }
    
    

            Registries.Model.extend(PosGlobalState, NewPosGlobalState);
        

});