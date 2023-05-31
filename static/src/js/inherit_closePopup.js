odoo.define('pos_custome.InheritClosePopup', function (require) {
    'use strict';

    const ClosePopup = require('point_of_sale.ClosePopup');
    const Registries = require('point_of_sale.Registries');
    

    const InheritClosePopup = (ClosePopup) =>
        class extends ClosePopup {
        
        };
    Registries.Component.extend(ClosePopup, InheritClosePopup);

    return InheritClosePopup;
});