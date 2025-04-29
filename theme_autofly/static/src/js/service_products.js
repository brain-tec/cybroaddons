/** @odoo-module **/

import publicWidget from '@web/legacy/js/public/public_widget';
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.service_product = publicWidget.Widget.extend({
    selector: '.product_service',
    async start(){
        const data = await rpc('/get_service_product')
        if(data){
            this.$target.empty().append(data);
        }
    }
});
