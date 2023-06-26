odoo.define('odoo-pos.models', function (require) {
    "use strict";

var models = require('point_of_sale.models');



var existing_models = models.PosModel.prototype.models;
var product_index = _.findIndex(existing_models, function (model) {
    return model.model === "product.product";
});
var product_model = existing_models[product_index];

models.load_models([{
  model:  product_model.model,
  fields: product_model.fields,
  order:  product_model.order,
  domain: function(self) {return [['id', '=', self.config.down_payment_product_id[0]]];},
  context: product_model.context,
  loaded: product_model.loaded,
}]);

models.load_fields("product.product", ['on_offer','actual_price','offer_price','offer_id']);

});