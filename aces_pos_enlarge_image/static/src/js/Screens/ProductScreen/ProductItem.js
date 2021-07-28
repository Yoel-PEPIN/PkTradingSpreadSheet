odoo.define('aces_pos_enlarge_image.ProductItem', function(require) {
   'use strict';

   const ProductItem = require('point_of_sale.ProductItem');
   const Registries = require('point_of_sale.Registries');

   const PosDemoProductItem = ProductItem =>
       class extends ProductItem {
           constructor() {
                super(...arguments);
           }
           async clickImage(){
               console.log("clickImage");
              const { confirmed,payload } = await this.showPopup('ImagePopup', {
                   title: this.env._t(this.props.product.display_name),
                   product:this.props.product,
              });
           }
       };

   Registries.Component.extend(ProductItem, PosDemoProductItem);

   return ProductItem;
});

