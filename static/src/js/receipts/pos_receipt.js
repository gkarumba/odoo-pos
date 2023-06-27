odoo.define('odoo-pos.OrderReceipt', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    var rpc = require('web.rpc')


    class OrderReceipt extends PosComponent {
        constructor() {
            super(...arguments);
            this._receiptEnv = this.props.order.getOrderReceiptEnv();
            this._receiptEnv.receipt.orderlines.forEach(element => {
                this._loadOfferDetails(element.product_name).then(result => {
                    var data = {
                        'on_offer': result[0]['on_offer'] || null, 
                        'actual_price': result[0]['actual_price'] , 
                        'offer_price': result[0]['offer_price'] || 0.0,
                        'offer_name': result[0]['offer_id'][1] || null,
                        'amount_saved': result[0]['actual_price'] - element.price_display_one || 0.0
                    }
                    element['offers'] = data
                });     
            });
        }
        willUpdateProps(nextProps) {
            this._receiptEnv = nextProps.order.getOrderReceiptEnv();
            this._receiptEnv.receipt.orderlines.forEach(element => {
                this._loadOfferDetails(element.product_name).then(result => {
                    var data = {
                        'on_offer': result[0]['on_offer'] || null, 
                        'actual_price': result[0]['actual_price'] , 
                        'offer_price': result[0]['offer_price'] || 0.0,
                        'offer_name': result[0]['offer_id'][1] || null,
                        'amount_saved': result[0]['actual_price'] - element.price_display_one || 0.0
                    }
                    element['offers'] = data
                });     
            });
        }
        get receipt() {
            console.log(this.receiptEnv.receipt)
            return this.receiptEnv.receipt;
        }
        get orderlines() {
            return this.receiptEnv.orderlines;
        }
        get paymentlines() {
            return this.receiptEnv.paymentlines;
        }
        get isTaxIncluded() {
            return Math.abs(this.receipt.subtotal - this.receipt.total_with_tax) <= 0.000001;
        }
        get receiptEnv () {
          return this._receiptEnv;
        }
        isSimple(line) {
            return (
                line.discount === 0 &&
                line.is_in_unit &&
                line.quantity === 1 &&
                !(
                    line.display_discount_policy == 'without_discount' &&
                    line.price < line.price_lst
                )
            );
        }

        _loadOfferDetails (name) {
            var _this = this;
            return _this.rpc({
                model: 'product.product',
                method: 'search_read',
                args: [],
                domain: [['name','=',name]],
                kwargs: {
                    fields: ['on_offer', 'actual_price', 'offer_price','offer_id'],
                },
            }).then(function (offers) {
                // console.log('offers',offers)
                return offers;
            });
        }

        
    }
    OrderReceipt.template = 'OrderReceipt';

    Registries.Component.add(OrderReceipt);

    return OrderReceipt;
});
