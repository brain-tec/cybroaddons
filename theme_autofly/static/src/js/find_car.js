/** @odoo-module **/

import { rpc } from "@web/core/network/rpc";
import publicWidget from "@web/legacy/js/public/public_widget";
import animations from "@website/js/content/snippets.animation";

publicWidget.registry.findCar = animations.Animation.extend({
    selector : '.find_car_class',
    async start() {
        const data = await rpc('/find_car')
        if(data){
            this.$target.empty().append(data);
        }
    }
});
