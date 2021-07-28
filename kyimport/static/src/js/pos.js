odoo.define('kyimport.pos', function (require) {
    "use strict";

    const { Gui } = require('point_of_sale.Gui');
    var models = require('point_of_sale.models');
    var rpc = require('web.rpc');
    var session = require('web.session');
    var core = require('web.core');
    var utils = require('web.utils');

    var _t = core._t;
    var round_di = utils.round_decimals;

    var _super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        disallowLineQuantityChange() {
            let result = _super_posmodel.disallowLineQuantityChange();
            return false && result;//fix problem cause by l10n_fr_pos_cert module
        }
    });
});
