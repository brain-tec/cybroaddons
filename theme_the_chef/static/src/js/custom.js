/** @odoo-module **/
import { renderToElement } from "@web/core/utils/render";
import { rpc } from "@web/core/network/rpc";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.banner = publicWidget.Widget.extend({
    selector: '.banner_section_body',

    async willStart() {
        this.$target.empty().html(renderToElement('theme_the_chef.banner_data'))
    },
    start() {
        this.onSlider();
    },

    // Slider1 Function
    onSlider() {
        // Initialize the first slider
        this.$("#slider").owlCarousel({
            items: 1,
            loop: true,
            margin: 30,
            stagePadding: 30,
            smartSpeed: 450,
            autoplay: true,
            autoPlaySpeed: 1000,
            autoPlayTimeout: 1000,
            autoplayHoverPause: true,
            dots: false,
            nav: false,
            navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>']
        });

        // Counter function for the second slider
        const counter = () => {
            this.$el.find('.owl-dots button').each((index, item) => {
                $(item).find('span').text(index + 1);
            });
        };

        // Initialize the second slider
        this.$("#slider2").owlCarousel({
            items: 1,
            loop: true,
            smartSpeed: 450,
            autoplay: true,
            autoPlaySpeed: 1000,
            autoPlayTimeout: 1000,
            autoplayHoverPause: true,
            onInitialized: counter,
            dots: true,
        });

        // Time Change Function
        const inputEle = document.getElementById('timeInput');
        if (inputEle) {
            inputEle.addEventListener('change', () => {
                const timeSplit = inputEle.value.split(':');
                let hours = parseInt(timeSplit[0], 10);
                const minutes = timeSplit[1];
                let meridian;

                if (hours > 12) {
                    meridian = 'PM';
                    hours -= 12;
                } else if (hours < 12) {
                    meridian = 'AM';
                    if (hours === 0) {
                        hours = 12;
                    }
                } else {
                    meridian = 'PM';
                }
                alert(`${hours}:${minutes} ${meridian}`);
            });
        }
    }
});

publicWidget.registry.WebsiteNewsletter = publicWidget.Widget.extend({
    selector: '#wrapwrap',
    events: {
        'click .subscribe-btn': 'onClickSubscribe',
    },
    async onClickSubscribe(ev) {
        // Function for subscribe newsletter.
        const $button = $(ev.currentTarget);
        const $input = $(ev.currentTarget.parentElement).find('input');
        this.$el.removeClass('o_has_error').find('.form-control').removeClass('is-invalid');
        if ($input.val().match(/.+@.+/)) {
            let data = await rpc('/subscribe_newsletter', {
                email: $input.val()
            });
            if (data) {
                $(ev.currentTarget.parentElement.parentElement).find('.warning').hide();
                $input.css('pointer-events', 'none');
                $button.css('background-color', 'green !important');
                $button.text("THANKS");
            } else {
                $(ev.currentTarget.parentElement.parentElement).find('.warning').text("Already subscribed to the newsletter.");
                $(ev.currentTarget.parentElement.parentElement).find('.warning').show();
            }
        } else {
            this.$el.addClass('o_has_error').find('.form-control').addClass('is-invalid');
            $(ev.currentTarget.parentElement.parentElement).find('.warning').text("Enter a valid email.");
            $(ev.currentTarget.parentElement.parentElement).find('.warning').show();
        }
    },
})
