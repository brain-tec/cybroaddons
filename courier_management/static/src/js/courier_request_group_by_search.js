/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.CourierRequest = publicWidget.Widget.extend({
    selector: '.groupby_courier',
    events : {
        'change #group_select_courier_requests' : '_onChangeCourierRequests',
        'change #courier_requests_search_box' : '_onChangeCourierRequestsSearch',
        'click #search_courier_requests_button' : '_onClickCourierRequests'
    },
    //    This is for getting group value of courier requests
    _onChangeCourierRequests: function(){
        let self = this
        var search_value = this.$el.find("#group_select_courier_requests").val();
        rpc('/courier/requests/group/by', {
            'search_value': search_value,
        }).then(function(result) {
            self.$el.find("#search_courier_requests_group").html(result);
            });
    },
    //    This is for getting search value of courier requests
    _onClickCourierRequests: function(){
        let self = this
        var search_value = self.$el.find("#courier_requests_search_box").val();
        rpc('/courier/requests/search', {
            'search_value': search_value,
        }).then(function(result) {
            self.$el.find("#search_courier_requests_group").html(result);
            });
    },

    _onChangeCourierRequestsSearch: function(){
        this._onClickCourierRequests()
    }
})
