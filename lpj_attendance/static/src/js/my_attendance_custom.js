odoo.define('lpj_attendance.my_attendance_custom', function (require) {
"use strict";

var core = require('web.core');
var Model = require('web.Model');
var Widget = require('web.Widget');

var QWeb = core.qweb;
var _t = core._t;


var MyAttendances = Widget.extend({
    events: {
        "click .o_hr_attendance_download_icon": function() {
            this.$('.o_hr_attendance_download_icon').attr("disabled", "disabled");
            this.window.open("http://127.0.0.1:8000/");
        },
    },



});

core.action_registry.add('hr_attendance_my_absensi', MyAttendances);

return MyAttendances;

});
