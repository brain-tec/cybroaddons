/** @odoo-module **/

import { rpc } from "@web/core/network/rpc";
import publicWidget from "@web/legacy/js/public/public_widget";
import animations from "@website/js/content/snippets.animation";

publicWidget.registry.getProductTab = animations.Animation.extend({
    selector : '.product_tab_class',
    async start(){
        const data =  await rpc('/get_product_tab')
        if(data){
            this.$target.empty().append(data);
        }
    }
});
