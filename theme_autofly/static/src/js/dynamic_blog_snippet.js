/** @odoo-module **/
import { rpc } from "@web/core/network/rpc";
import publicWidget from "@web/legacy/js/public/public_widget";
import animations from "@website/js/content/snippets.animation";
animations.registry.blogSnippet = animations.Animation.extend({
    selector : '.blog_index',
    async start() {
        const data = await rpc('/dynamic_blog')
        if(data){
            this.$target.empty().append(data);
        }
    }
});
