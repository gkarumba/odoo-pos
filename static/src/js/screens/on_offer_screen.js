odoo.define('odoo-pos.OnOfferScreen', function(require) {
    'use strict';
    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const {useListener} = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');



    class OnOfferScreen extends PosComponent {

        constructor() {
            super (... arguments);
            // this.offer = this.env.pos.product_categories;
       }

        back() {
            this.trigger('close-temp-screen');
        }
    }
    OnOfferScreen.template = 'OnOfferScreen';
    Registries.Component.add(OnOfferScreen);
    return OnOfferScreen;
  });