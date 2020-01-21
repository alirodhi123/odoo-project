odoo.define('account_dynamic_gl.Dynamic_Base', function (require) {
'use strict';

var ActionManager = require('web.ActionManager');
var data = require('web.data');
var Dialog = require('web.Dialog');
var FavoriteMenu = require('web.FavoriteMenu');
var form_common = require('web.form_common');
var pyeval = require('web.pyeval');
var ViewManager = require('web.ViewManager');
var web_client = require('web.web_client');

var ajax = require('web.ajax');
var core = require('web.core');
var Widget = require('web.Widget');
var base = require('web_editor.base');
var Model = require('web.Model');
var session = require('web.session');

var formats = require('web.formats');
var utils = require('web.utils');
var round_di = utils.round_decimals;

var _t = core._t;
var QWeb = core.qweb;

var exports = {};

var DynamicMain = Widget.extend({
    template:'DynamicMain',

    init : function(view, code){
        this._super(view, code);
    },

	start : function(){
        new ControlButtons(this).appendTo(this.$('.ControlSection'));
        new UserFilters(this).appendTo(this.$('.FiltersSection'));
	    }, //start

    }); //DynamicMain

var UserFilters = Widget.extend({
    template:'UserFilters',

    init : function(view, code){
		this._super(view, code);
		},

	start : function(){
	    var self = this;

	    // Calling common template. for both company and Date filter
	    self.$el.append(QWeb.render('CompanyDatefilterLine'));

	    // Getting date filters
	    // Add filter type section
	    self.$el.find('.date-filters').append(QWeb.render('DatefilterSelectionLine'));
	    self.$el.find('.dynamic-datefilter-multiple').select2({
	        placeholder:'Select filter type...',
	        maximumSelectionSize: 1,
	        }).val('this_month').trigger('change');

        // Getting companies from company master
        var company_ids = [];
        var current_company = self.session.company_id
        var allowed_companies = []
        var company_filter = []
        if(!(session.is_admin)){
            allowed_companies.push(parseInt(session.company_id));
            company_filter = [['id','in',allowed_companies]];
        }
        var a = new Model('res.company')
            .query(['name','id'])
            .filter(company_filter)
            .all()
            .then(function(results){
            _(results).each(function (item) {
                company_ids.push({'name':item.name,'code':item.id})
                }) //each
            self.$el.find('.multi-companies').append(QWeb.render('MultiCompanies', {'companies': company_ids}));
            self.$el.find('.dynamic-company-multiple').select2({
                placeholder:'Select companies...',
                }).val(current_company).trigger('change');
            }); //query

        // Date from and To
	    self.$el.append(QWeb.render('DateLine'));

        // No need to fetch from DB. Just templates
	    self.$el.append(QWeb.render('TargetAccountsLine'));
	    self.$el.append(QWeb.render('SortByInitialBalanceLine'));

        // Getting partners from partner master
	    var partners = [];
        var a = new Model('res.partner').query(['name','id']).all().then(function(results){
            _(results).each(function (item) {
                partners.push({'name':item.name,'id':item.id})
                }) //each
            self.$el.append(QWeb.render('PartnersLine', {'partners': partners}));
            self.$el.find('.dynamic-partner-multiple').select2({
                placeholder:'Select partners...',
                minimumResultsForSearch: 5
                });

            }); //query

	    // Getting journals from journal master
	    var journals = [];
	    var journal_ids = []
        var a = new Model('account.journal').query(['name','id','code']).all().then(function(results){
            _(results).each(function (item) {
                journals.push({'name':item.name,'code':item.id,'short_code':item.code})
                journal_ids.push(parseInt(item.id))
                }) //each
            self.$el.append(QWeb.render('JournalsLine', {'journals': journals}));
            self.$el.find('.dynamic-journal-multiple').select2({
                placeholder:'Select journals...',
                minimumResultsForSearch: 5
                }).val(journal_ids).trigger('change');

            }); //query

        self.$el.append(QWeb.render('Account'));

        var accounts = [];
        var a = new Model('account.account').query(['name','id','code']).all().then(function(results){
            _(results).each(function (item) {
                accounts.push({'name':item.name,'code':item.id,'short_code':item.code})

                }) //each
            if(accounts.length == 0) {
                self.getParent().$el.find('button').hide();
                web_client.do_notify(_("Insufficient data"), "No chart of account defined for this company");
            }
            self.$el.find('.normal_acc').append(QWeb.render('AccountsLine', {'accounts': accounts}));
            self.$el.find('.dynamic-account-multiple').select2({
                placeholder:'Select accounts...',
                minimumResultsForSearch: 5
                });

            }); //query

        // Getting account tags from tags master
	    var account_tags = [];
        var a = new Model('account.account.tag').query(['name','id']).all().then(function(results){
            _(results).each(function (item) {
                account_tags.push({'name':item.name,'code':item.id})

                }) //each
            self.$el.find('.normal_acc_tags').append(QWeb.render('AccountTagsLine', {'acc_tags': account_tags}));
            self.$el.find('.dynamic-acc-tags-multiple').select2({
                placeholder:'Select account tags...',
                });
            }); //query

        self.$el.append(QWeb.render('Analytic'));

        // Getting analytic account from master
	    var analytic_accounts = [];
        var a = new Model('account.analytic.account').query(['name','id']).all().then(function(results){
            _(results).each(function (item) {
                analytic_accounts.push({'name':item.name,'code':item.id})

                }) //each
            self.$el.find('.analytic_acc').append(QWeb.render('AnalyticAccountLine', {'analytic_accs': analytic_accounts}));
            self.$el.find('.dynamic-analytic-acc-multiple').select2({
                placeholder:'Select analytic accounts...',
                });
            }); //query

//        //Getting analytic account analytic tags from tags master
//	    var analytic_account_tags = [];
//        var a = new Model('account.analytic.tag').query(['name','id']).all().then(function(results){
//            _(results).each(function (item) {
//                analytic_account_tags.push({'name':item.name,'code':item.id})
//
//                }) //each
//            self.$el.find('.analytic_acc_tags').append(QWeb.render('AnalyticTagsLine', {'analytic_acc_tags': analytic_account_tags}));
//            self.$el.find('.dynamic-analytic-acc-tags-multiple').select2({
//                placeholder:'Select analytic tags...',
//                });
//            }); //query

        var date = new Date();
        var y = date.getFullYear();
        var m = date.getMonth();
        self.$el.find('#from_date').datetimepicker({
                    icons: {
                        time: "fa fa-clock-o",
                        date: "fa fa-calendar",
                        up: "fa fa-arrow-up",
                        down: "fa fa-arrow-down"
                    },
                    viewMode: 'days',
                    format: 'DD/MM/YYYY',
                    defaultDate: new Date(y, m, 1)
                });
        self.$el.find('#to_date').datetimepicker({
                    icons: {
                        time: "fa fa-clock-o",
                        date: "fa fa-calendar",
                        up: "fa fa-arrow-up",
                        down: "fa fa-arrow-down"
                    },
                    viewMode: 'days',
                    format: 'DD/MM/YYYY',
                    defaultDate: new Date(y, m+1, 0)
                });

	    }, //start

	}); //UserFilters

var ControlButtons = Widget.extend({
    template:'ControlButtons',
    events: {
        'click #filter_button': 'filter_button_click',
        'click #apply_button': 'apply_button_click',
        'click #expand_all': 'apply_button_expand_all',
        'click #merge_all': 'apply_button_merge_all',
        'click #pdf_button': 'download_pdf',
        'click #xlsx_button': 'download_xlsx'
    },

    init : function(view, code){
		this._super(view, code);
		},

	start : function(){
	    var self = this;
	    $("#expand_all").toggle();
        $("#merge_all").toggle();
	    }, //start

	filter_button_click : function(event){
        $(".account_filter").slideToggle("slow",function(){
            $("#apply_button").toggle();
            });
	    },

	apply_button_expand_all : function(event){
	    $('.move-sub-line').collapse('show');
	},

	apply_button_merge_all : function(event){
	    $('.move-sub-line').collapse('hide');
	},

	download_pdf : function(event){
	    var self = this;
	    var filter = self.get_filter_datas();

	    return new Model('report.account.dynamic.report_generalledger').call('render_html',[filter,'pdf']).then(function(result){
                var action = {
                    'type': 'ir.actions.report.xml',
                    'report_type': 'qweb-pdf',
                    'report_name': 'account.report_generalledger',
                    'report_file': 'account.report_generalledger',
                    'data': result,
                    'context': {'active_model':'account.report.general.ledger',
                                'landscape':1},
                    'display_name': 'General Ledger',
                };
                return web_client.do_action(action);
            });
	},

	download_xlsx : function(event){
	    var self = this;
	    var filter = self.get_filter_datas();

	    return new Model('report.account.dynamic.report_generalledger').call('render_html',[filter,'xlsx']).then(function(result){
                var action = {
                    'type': 'ir.actions.report.xml',
                    'report_type': 'xlsx',
                    'report_name': 'account_dynamic_gl.general_ledger_xls.xlsx',
                    'report_file': 'account_dynamic_gl.general_ledger_xls.xlsx',
                    'context': {'active_model':'account.report.general.ledger',
                                'data': result,
                                },
                    'display_name': 'General Ledger',
                };
                return web_client.do_action(action);
            });
	},

	apply_button_click : function(event){
	    var self = this;
	    var output = self.get_filter_datas();

	    // Hide filter sections when apply filter button
        $(".account_filter").slideToggle("slow",function(){
            $("#apply_button").toggle();
            });

	    var final_html = new Model('report.account.dynamic.report_generalledger').call('render_html',[output]).then(function(result){
                $(".DataSection").empty();
                new AccountContents(this,result).appendTo($(".DataSection"));
            });
	},

	get_filter_datas : function(){
	    var self = this;
	    var output = {}

        // Get journals
	    var journal_ids = [];
	    var journal_list = $(".dynamic-journal-multiple").select2('data')
	    for (var i=0; i < journal_list.length; i++){
	        journal_ids.push(parseInt(journal_list[i].id))
	        }
	    output.journal_ids = journal_ids
	    // Get partners
	    var partner_ids = [];
	    var partner_list = $(".dynamic-partner-multiple").select2('data')
	    for (var i=0; i < partner_list.length; i++){
	        partner_ids.push(parseInt(partner_list[i].id))
	        }
	    output.partner_ids = partner_ids
        // Get ous
        var ou_ids = [];
	    var ou_list = $(".dynamic-ou-multiple").select2('data')
	    for (var i=0; i < ou_list.length; i++){
	        ou_ids.push(parseInt(ou_list[i].id))
	        }
	    output.ou_ids = ou_ids
        // Get companies
        var company_ids = [];
	    var company_list = $(".dynamic-company-multiple").select2('data')
	    for (var i=0; i < company_list.length; i++){
	        company_ids.push(parseInt(company_list[i].id))
	        }
	    output.company_ids = company_ids

	    // Get accounts
        var account_ids = [];
	    var account_list = $(".dynamic-account-multiple").select2('data')
	    for (var i=0; i < account_list.length; i++){
	        account_ids.push(parseInt(account_list[i].id))
	        }
	    output.account_ids = account_ids

	    // Get account tags
        var account_tag_ids = [];
	    var account_tag_list = $(".dynamic-acc-tags-multiple").select2('data')
	    for (var i=0; i < account_tag_list.length; i++){
	        account_tag_ids.push(parseInt(account_tag_list[i].id))
	        }
	    output.account_tag_ids = account_tag_ids

	    // Get analytic account
        var account_analytic_ids = [];
	    var account_analytic_list = $(".dynamic-analytic-acc-multiple").select2('data')
	    for (var i=0; i < account_analytic_list.length; i++){
	        account_analytic_ids.push(parseInt(account_analytic_list[i].id))
	        }
	    output.analytic_account_ids = account_analytic_ids

	    // Get analytic account tags
        var account_analytic_tags_ids = [];
	    var account_analytic_tags_list = $(".dynamic-analytic-acc-tags-multiple").select2('data')
	    for (var i=0; i < account_analytic_tags_list.length; i++){
	        account_analytic_tags_ids.push(parseInt(account_analytic_tags_list[i].id))
	        }
	    output.analytic_tag_ids = account_analytic_tags_ids

	    // Get Date filters
	    output.date_filter = $(".dynamic-datefilter-multiple").select2('data')

	    // Get dates
	    if ($("#from_date").data("DateTimePicker").getDate()){
	        output.date_from = $("#from_date").data("DateTimePicker").getDate().format('YYYY-MM-DD');
	        }
        if ($("#to_date").data("DateTimePicker").getDate()){
            output.date_to = $("#to_date").data("DateTimePicker").getDate().format('YYYY-MM-DD');
            }


        // Get checkboxes
	    if ($("#all_posted_entries").is(':checked')){ // All posted
	        output.all_posted = true
	        }else{output.all_posted = false}
	    if ($("#all_entries").is(':checked')){ // All entries
	        output.all_entries = true
	        }else{output.all_entries = false}
	    if ($("#all_datas").is(':checked')){ // All accounts
	        output.all_datas = true
	        }else{output.all_datas = false}
	    if ($("#all_movements").is(':checked')){ // All with movement
	        output.all_movements = true
	        }else{output.all_movements = false}
	    if ($("#all_balance_not_zero").is(':checked')){ // All with non zero
	        output.all_balance_not_zero = true
	        }else{output.all_balance_not_zero = false}
	    if ($("#by_date").is(':checked')){
	        output.by_date = true
	        }else{output.by_date = false}
	    if ($("#by_journal_and_partner").is(':checked')){
	        output.by_journal_and_partner = true
	        }else{output.by_journal_and_partner = false}
	    if ($("#initial_balance_yes").is(':checked')){
	        output.initial_balance = true
	        }else{output.initial_balance = false}

        return output
	},

	}); //ControlButtons

var AccountContents = Widget.extend({
    template:'AccountContents',
    events: {
        // events binding
        'click .view-source': 'view_move_line',
        'click .view-invoice': 'view_invoice',
        },
    init : function(view, code){
		this._super(view, code);
		this.result = JSON.parse(code); // To convert string to JSON
		},
	start : function(){
	    var self = this;

	    }, //start

	format_currency_no_symbol: function(amount, precision){
	    var decimals = precision;
	    if (typeof amount === 'number') {
            amount = round_di(amount,decimals).toFixed(decimals);
            amount = formats.format_value(round_di(amount, decimals), { type: 'float', digits: [69, decimals]});
        }

        return amount;
	},

	format_currency_with_symbol: function(amount, precision, symbol, position){
	    var decimals = precision;
	    if (typeof amount === 'number') {
            amount = round_di(amount,decimals).toFixed(decimals);
            amount = formats.format_value(round_di(amount, decimals), { type: 'float', digits: [69, decimals]});
        }
        if (position === 'after') {
            return amount + ' ' + (symbol || '');
        } else {
            return (symbol || '') + ' ' + amount;
        }

        return amount;
	},

	/* Used to redirect to move record */
	view_move_line : function(event){
        var self = this;
        var context = {};

        var redirect_to_document = function (res_model, res_id, view_id) {
            web_client.do_action({
                type:'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: res_model,
                views: [[view_id || false, 'form']],
                res_id: res_id,
                context: context,
            });
            web_client.do_notify(_("Redirected"), "Window has been redirected");
        };

        redirect_to_document('account.move',$(event.currentTarget).data('move-id'));

        }, //view_move_line

    /* Used to redirect to invoice record */
    view_invoice : function(event){
        var self = this;
        var context = {};
        var generalLedgerModel = new Model('report.account.dynamic.report_generalledger');

        generalLedgerModel.call('get_invoice_details',[$(event.currentTarget).data('lref')])
            .then(function(res_id){
                if (res_id){
                    web_client.do_action({
                        type:'ir.actions.act_window',
                        view_type: 'form',
                        view_mode: 'form',
                        res_model: 'account.invoice',
                        views: [[false, 'form']],
                        res_id: res_id,
                        context: context,
                    });
                    web_client.do_notify(_("Redirected"), "Window has been redirected");
                }
            });

        }, //view_invoice

	}); //AccountContents


core.action_registry.add("dynamic.gl.report", DynamicMain);
});
