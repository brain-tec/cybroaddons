/** @odoo-module **/
import { NavBar } from "@web/webclient/navbar/navbar";
import { patch } from "@web/core/utils/patch";

// Patch NavBar for adding new sidebar functionality
patch(NavBar.prototype, {
    setup() {
        super.setup();
    },

    // Toggle sidebar on click
    openSidebar(ev) {
        const sidebarPanel = ev.target.closest('header').querySelector('#sidebar_panel');
        const actionManager = document.body.querySelector('.o_action_manager');

        if (!ev.target.classList.contains('opened')) {
            sidebarPanel.style.display = 'block';
            ev.target.classList.toggle('opened');
            actionManager.style.marginLeft = '320px';
            actionManager.style.transition = 'all .1s linear';
        } else {
            sidebarPanel.style.display = 'none';
            ev.target.classList.toggle('opened');
            actionManager.style.marginLeft = '0px';
        }
    },
    clickSidebar(ev) {
        const sidebarPanel = ev.target.closest('header').querySelector('#sidebar_panel');
        const actionManager = document.body.querySelector('.o_action_manager');
        sidebarPanel.style.display = 'none';
        actionManager.style.marginLeft = '0px';
    },
});
