/** @odoo-module **/

import { NavBar } from "@web/webclient/navbar/navbar";
import { patch } from "@web/core/utils/patch";
import { useRef, onMounted } from "@odoo/owl";

patch(NavBar.prototype, {
    setup() {
        super.setup();

        // Attach a ref for the root element
        this.sideRoot = useRef("side_root");

        // Ensure that DOM manipulation happens after mounting
        onMounted(this.handleMounted.bind(this));
    },

    handleMounted() {
        // Access the DOM element for the sidebar panel
        if (!this.sideRoot.el) {
            console.error("sideRoot.el is not defined. Check the template structure.");
            return;
        }

        this.$searchContainer = this.sideRoot.el.querySelector(".search-container");
        this.$searchInput = this.sideRoot.el.querySelector(".search-input");
        this.$searchResults = this.sideRoot.el.querySelector(".search-results");
        this.$appMenu = this.sideRoot.el.querySelector(".app-menu");

        if (!this.$searchContainer || !this.$searchInput) {
            console.error("Required elements not found in the DOM.");
        }
    },
});
