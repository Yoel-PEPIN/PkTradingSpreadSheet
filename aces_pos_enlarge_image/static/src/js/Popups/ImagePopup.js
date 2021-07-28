odoo.define('aces_pos_enlarge_image.ImagePopup', function(require) {
   'use strict';

    const { useState, useRef } = owl.hooks;
    const { useListener } = require('web.custom_hooks');
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');

    class ImagePopup extends AbstractAwaitablePopup {
        constructor() {
           super(...arguments);
       }
        get imageUrl() {
            const product = this.props.product;
            return `/web/image?model=product.product&field=image_1024&id=${product.id}&write_date=${product.write_date}&unique=1`;
        }
    }

    ImagePopup.template = 'ImagePopup';
    Registries.Component.add(ImagePopup);

    return ImagePopup;

});
