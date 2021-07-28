odoo.define('aspl_pos_create_so_extension.SaleOrderConfirmPopup', function(require) {
    'use strict';

    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');

    var core = require('web.core');
    var _t = core._t;

    class SaleOrderConfirmPopup extends AbstractAwaitablePopup {}

    SaleOrderConfirmPopup.template = 'SaleOrderConfirmPopup';

    SaleOrderConfirmPopup.defaultProps = {
        confirmText: _t('Download'),
        title: _t('Successful'),
        cancelText: _t('Close')
    };

    Registries.Component.add(SaleOrderConfirmPopup);

    return SaleOrderConfirmPopup;
});
