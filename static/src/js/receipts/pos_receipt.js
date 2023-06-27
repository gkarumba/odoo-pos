odoo.define('odoo-pos.OrderReceipt', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    var rpc = require('web.rpc')


    class OrderReceipt extends PosComponent {
        constructor() {
            super(...arguments);
            this._receiptEnv = this.props.order.getOrderReceiptEnv();
        }
        willUpdateProps(nextProps) {
            this._receiptEnv = nextProps.order.getOrderReceiptEnv();
        }
        get receipt() {
            
            var new_receipt = this.receiptEnv.receipt.orderlines.forEach(element => {
                this._loadOfferDetails(element.product_name).then(result => {
                    var data = {
                        'on_offer': result[0]['on_offer'] || null, 
                        'actual_price': result[0]['actual_price'], 
                        'offer_price': result[0]['offer_price'],
                        'offer_name': result[0]['offer_id'][1],
                        'amount_saved': result[0]['actual_price'] - element.price_display_one
                    }
                    element['offers'] = data
                });     
            });
            // console.log(this.receiptEnv.receipt)
            return new_receipt;
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
