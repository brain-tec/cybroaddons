odoo.define('theme_autofly.find_car', function(require){
    'use strict';

    var Animation = require('website.content.snippets.animation');
    var ajax = require('web.ajax');
    Animation.registry.find_car = Animation.Class.extend({
        selector : '.find_car_class',
        /**Function for getting the car details**/
        start: function(){
            var self = this;
            ajax.jsonRpc('/find_car', 'call', {})
            .then(function (data) {
                if(data){
                    self.$el.html(data);
                }
            });
        }
    });
});