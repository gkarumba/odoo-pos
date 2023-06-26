odoo.define("odoo-pos.ProductInfoPopup", function (require) {
    "use strict";

    const ProductInfoPopup = require("point_of_sale.ProductInfoPopup");
    const Registries = require("point_of_sale.Registries");

    const InheritProductInfoPopup = (ProductInfoPopup) =>
        class InheritProductInfoPopup extends ProductInfoPopup {
            
            searchProductOffer(productName) {
                
            }
        };

    Registries.Component.extend(ProductInfoPopup, InheritProductInfoPopup);

    return InheritProductInfoPopup;

})