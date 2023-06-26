odoo.define('odoo-pos.OnOfferButton', function (require) {
    'use strict';
    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    const { useListener } = require('web.custom_hooks');


    class OnOfferButton extends PosComponent {

        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }

        async onClick() {
            var self = this;
            await this.rpc({
                           model: 'product.offer',
                            method: 'search_read',
                            args: [[], ['name', 'price', 'offer_line_ids']],
                    }).then(function (result) {
                         self.showScreen('OfferScreen', {
                            offers: result,
                        });
                    });
            }

        _onClick() {
            this.showTempScreen('OfferScreen');
        }
    }
    OnOfferButton.template = 'odoo-pos.OnOfferButton';
    ProductScreen.addControlButton({
        component: OnOfferButton,
        condition: function () {
            return true;
        },
        position: ['before', 'SetPricelistButton'],
    });
    Registries.Component.add(OnOfferButton);
    return OnOfferButton;
});