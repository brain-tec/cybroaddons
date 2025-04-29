/** @odoo-module **/
import publicWidget from '@web/legacy/js/public/public_widget';
import { rpc } from "@web/core/network/rpc";
publicWidget.registry.car_garage = publicWidget.Widget.extend({
    selector : '.car_garage',
    init() {
        this._super(...arguments);
    },
    async start() {
        const data = await rpc('/get_garage_car',{})
        if(data){
            this.$target.empty().append(data);
        }
    }
});
