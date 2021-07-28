odoo.define('aspl_pos_create_so_extension.SaleOrderReturnPopup', function(require) {
    'use strict';

    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const { useState, useRef } = owl.hooks;
    const { useListener } = require('web.custom_hooks');

    var core = require('web.core');
    var _t = core._t;

    class SaleOrderReturnPopup extends AbstractAwaitablePopup {
        constructor(){
            super(...arguments);
            this.state = useState({ ProductLines : this.props.lines });
            this.state.ProductLines = this.props.lines;
            useListener('delete-popup-orderline', () => this._deletePopupline(event));
        }
        _deletePopupline(event){
            let lines = this.props.lines;
            var removeIndex = lines.map(function(item) { return item.id; }).indexOf(event.detail.orderline_id);
            lines.splice(removeIndex, 1);
            this.state.ProductLines = lines;
            this.render();
        }
        getPayload(){
            return this.state.ProductLines;
        }
    }
    SaleOrderReturnPopup.template = 'SaleOrderReturnPopup';

    SaleOrderReturnPopup.defaultProps = {
        confirmText: 'Ok',
        title: '',
        cancelText: _t('Cancel')
    };

    Registries.Component.add(SaleOrderReturnPopup);

    return SaleOrderReturnPopup;
});
