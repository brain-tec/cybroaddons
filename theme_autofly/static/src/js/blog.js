/** @odoo-module **/

import { rpc } from "@web/core/network/rpc";
import publicWidget from "@web/legacy/js/public/public_widget";
import animations from "@website/js/content/snippets.animation";
import { renderToElement } from "@web/core/utils/render";

publicWidget.registry.latestBlog = animations.Animation.extend({
    selector: '.blog_wrapper',
    async start () {
        const data = await rpc('/blog_snippet')
        if(data) {
            this.$target.empty().append(renderToElement('theme_autofly.blog_snippet', {
                blog_data: data,
                slug: this.slug
            }))
        }
    },
    slug(rec) {
        return rec[1].split(' ').join('-') + '-' + rec[0]
    },
})
