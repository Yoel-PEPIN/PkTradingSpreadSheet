odoo.define('new_field_pos', function (require) {
    "use strict";
    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    const ClientListScreen = require('point_of_sale.ClientListScreen');

    var models = require('point_of_sale.models');

    models.load_fields("res.partner", ["total_due", "user_id"]);
});