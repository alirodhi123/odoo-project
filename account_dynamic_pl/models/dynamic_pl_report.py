# -*- coding: utf-8 -*-

import time
from openerp import api, fields, models, _
import json
from datetime import datetime, timedelta, date
import calendar
from dateutil.relativedelta import relativedelta
from openerp.tools.misc import formatLang

class ReportDynamicFinancial(models.AbstractModel):
    _name = 'report.account.dynamic.report_financial'

    @api.multi
    def get_date_from_filter(self, filter):
        '''
        :param filter: dictionary
                {u'disabled': False, u'text': u'This month', u'locked': False, u'id': u'this_month', u'element': [{}]}
        :return: date_from and date_to
        '''
        if filter.get('id'):
            date = datetime.today()
            if filter['id'] == 'today':
                date_from = date.strftime("%Y-%m-%d")
                date_to = date.strftime("%Y-%m-%d")
                return date_from, date_to
            if filter['id'] == 'this_week':
                day_today = date - timedelta(days=date.weekday())
                date_from = (day_today - timedelta(days=date.weekday())).strftime("%Y-%m-%d")
                date_to = (day_today + timedelta(days=6)).strftime("%Y-%m-%d")
                return date_from, date_to
            if filter['id'] == 'this_month':
                date_from = datetime(date.year, date.month, 1).strftime("%Y-%m-%d")
                date_to = datetime(date.year, date.month, calendar.mdays[date.month]).strftime("%Y-%m-%d")
                return date_from, date_to
            if filter['id'] == 'this_quarter':
                if int((date.month - 1) / 3) == 0:  # First quarter
                    date_from = datetime(date.year, 1, 1).strftime("%Y-%m-%d")
                    date_to = datetime(date.year, 3, calendar.mdays[3]).strftime("%Y-%m-%d")
                if int((date.month - 1) / 3) == 1:  # First quarter
                    date_from = datetime(date.year, 4, 1).strftime("%Y-%m-%d")
                    date_to = datetime(date.year, 6, calendar.mdays[6]).strftime("%Y-%m-%d")
                if int((date.month - 1) / 3) == 2:  # First quarter
                    date_from = datetime(date.year, 7, 1).strftime("%Y-%m-%d")
                    date_to = datetime(date.year, 9, calendar.mdays[9]).strftime("%Y-%m-%d")
                if int((date.month - 1) / 3) == 3:  # First quarter
                    date_from = datetime(date.year, 10, 1).strftime("%Y-%m-%d")
                    date_to = datetime(date.year, 12, calendar.mdays[12]).strftime("%Y-%m-%d")
                return date_from, date_to
            if filter['id'] == 'this_financial_year':
                date_from = datetime(date.year, 1, 1).strftime("%Y-%m-%d")
                date_to = datetime(date.year, 12, 31).strftime("%Y-%m-%d")
                return date_from, date_to
            date = (datetime.now() - relativedelta(day=1))
            if filter['id'] == 'yesterday':
                date_from = date.strftime("%Y-%m-%d")
                date_to = date.strftime("%Y-%m-%d")
                return date_from, date_to
            date = (datetime.now() - relativedelta(day=7))
            if filter['id'] == 'last_week':
                day_today = date - timedelta(days=date.weekday())
                date_from = (day_today - timedelta(days=date.weekday())).strftime("%Y-%m-%d")
                date_to = (day_today + timedelta(days=6)).strftime("%Y-%m-%d")
                return date_from, date_to
            date = (datetime.now() - relativedelta(months=1))
            if filter['id'] == 'last_month':
                date_from = datetime(date.year, date.month, 1).strftime("%Y-%m-%d")
                date_to = datetime(date.year, date.month, calendar.mdays[date.month]).strftime("%Y-%m-%d")
                return date_from, date_to
            date = (datetime.now() - relativedelta(months=3))
            if filter['id'] == 'last_quarter':
                if int((date.month - 1) / 3) == 0:  # First quarter
                    date_from = datetime(date.year, 1, 1).strftime("%Y-%m-%d")
                    date_to = datetime(date.year, 3, calendar.mdays[3]).strftime("%Y-%m-%d")
                if int((date.month - 1) / 3) == 1:  # Second quarter
                    date_from = datetime(date.year, 4, 1).strftime("%Y-%m-%d")
                    date_to = datetime(date.year, 6, calendar.mdays[6]).strftime("%Y-%m-%d")
                if int((date.month - 1) / 3) == 2:  # Third quarter
                    date_from = datetime(date.year, 7, 1).strftime("%Y-%m-%d")
                    date_to = datetime(date.year, 9, calendar.mdays[9]).strftime("%Y-%m-%d")
                if int((date.month - 1) / 3) == 3:  # Fourth quarter
                    date_from = datetime(date.year, 10, 1).strftime("%Y-%m-%d")
                    date_to = datetime(date.year, 12, calendar.mdays[12]).strftime("%Y-%m-%d")
                return date_from, date_to
            date = (datetime.now() - relativedelta(years=1))
            if filter['id'] == 'last_financial_year':
                date_from = datetime(date.year, 1, 1).strftime("%Y-%m-%d")
                date_to = datetime(date.year, 12, 31).strftime("%Y-%m-%d")
                return date_from, date_to

    def _compute_account_balance(self, accounts):
        """ compute the balance, debit and credit for the provided accounts
        """
        mapping = {
            'balance': "COALESCE(SUM(debit),0) - COALESCE(SUM(credit), 0) as balance",
            'debit': "COALESCE(SUM(debit), 0) as debit",
            'credit': "COALESCE(SUM(credit), 0) as credit",
        }

        res = {}
        for account in accounts:
            res[account.id] = dict.fromkeys(mapping, 0.0)
        if accounts:
            tables, where_clause, where_params = self.env['account.move.line']._query_get()
            tables = tables.replace('"', '') if tables else "account_move_line"
            wheres = [""]
            if where_clause.strip():
                wheres.append(where_clause.strip())
            filters = " AND ".join(wheres)
            request = "SELECT account_id as id, " + ', '.join(mapping.values()) + \
                       " FROM " + tables + \
                       " WHERE account_id IN %s " \
                            + filters + \
                       " GROUP BY account_id"
            params = (tuple(accounts._ids),) + tuple(where_params)
            self.env.cr.execute(request, params)
            for row in self.env.cr.dictfetchall():
                res[row['id']] = row
        return res

    def _compute_report_balance(self, reports):
        '''returns a dictionary with key=the ID of a record and value=the credit, debit and balance amount
           computed for this record. If the record is of type :
               'accounts' : it's the sum of the linked accounts
               'account_type' : it's the sum of leaf accoutns with such an account_type
               'account_report' : it's the amount of the related report
               'sum' : it's the sum of the children of this record (aka a 'view' record)'''
        res = {}
        fields = ['credit', 'debit', 'balance']
        for report in reports:
            if report.id in res:
                continue
            res[report.id] = dict((fn, 0.0) for fn in fields)
            if report.type == 'accounts':
                # it's the sum of the linked accounts
                res[report.id]['account'] = self._compute_account_balance(report.account_ids)
                for value in res[report.id]['account'].values():
                    for field in fields:
                        res[report.id][field] += value.get(field)
            elif report.type == 'account_type':
                # it's the sum the leaf accounts with such an account type
                accounts = self.env['account.account'].search([('user_type_id', 'in', report.account_type_ids.ids)])
                res[report.id]['account'] = self._compute_account_balance(accounts)
                for value in res[report.id]['account'].values():
                    for field in fields:
                        res[report.id][field] += value.get(field)
            elif report.type == 'account_report' and report.account_report_id:
                # it's the amount of the linked report
                res2 = self._compute_report_balance(report.account_report_id)
                for key, value in res2.items():
                    for field in fields:
                        res[report.id][field] += value[field]
            elif report.type == 'sum':
                # it's the sum of the children of this account.report
                res2 = self._compute_report_balance(report.children_ids)
                for key, value in res2.items():
                    for field in fields:
                        res[report.id][field] += value[field]
        return res

    def get_account_lines(self, data):
        lines = []
        #account_report = self.env['account.financial.report'].search([('id', '=', data['account_report_id'][0])])
        account_report = self.env.ref('account.account_financial_report_profitandloss0')
        child_reports = account_report._get_children_by_order()
        res = self.with_context(data.get('used_context'))._compute_report_balance(child_reports)
        if data['enable_filter']:
            comparison_res = self.with_context(data.get('comparison_context'))._compute_report_balance(child_reports)
            for report_id, value in comparison_res.items():
                res[report_id]['comp_bal'] = value['balance']
                report_acc = res[report_id].get('account')
                if report_acc:
                    for account_id, val in comparison_res[report_id].get('account').items():
                        report_acc[account_id]['comp_bal'] = val['balance']

        for report in child_reports:
            company_id = self.env['res.company'].browse(data.get('company_ids',False))
            currency_id = company_id.currency_id
            vals = {
                'name': report.name,
                'balance': res[report.id]['balance'] * report.sign,
                'parent': report.parent_id.id if report.parent_id.type in ['accounts','account_type'] else 0,
                'self_id': report.id,
                'type': 'report',
                'style_type': 'main',
                'precision': currency_id.decimal_places,
                'symbol': currency_id.symbol,
                'position': currency_id.position,
                'list_len': [a for a in range(0,bool(report.style_overwrite) and report.style_overwrite or report.level)],
                'level': bool(report.style_overwrite) and report.style_overwrite or report.level,
                'account_type': report.type or False, #used to underline the financial report balances
            }
            if data['debit_credit']:
                vals['debit'] = res[report.id]['debit']
                vals['credit'] = res[report.id]['credit']

            if data['enable_filter']:
                vals['balance_cmp'] = res[report.id]['comp_bal'] * report.sign

            lines.append(vals)
            if report.display_detail == 'no_detail':
                #the rest of the loop is used to display the details of the financial report, so it's not needed here.
                continue

            if res[report.id].get('account'):
                sub_lines = []
                for account_id, value in res[report.id]['account'].items():
                    #if there are accounts to display, we add them to the lines with a level equals to their level in
                    #the COA + 1 (to avoid having them with a too low level that would conflicts with the level of data
                    #financial reports for Assets, liabilities...)
                    flag = False
                    account = self.env['account.account'].browse(account_id)
                    vals = {
                        'name': account.code + ' ' + account.name,
                        'balance': value['balance'] * report.sign or 0.0,
                        'type': 'account',
                        'parent': report.id if report.type in ['accounts','account_type'] else 0,
                        'self_id': 50,
                        'style_type': 'sub',
                        'precision': currency_id.decimal_places,
                        'symbol': currency_id.symbol,
                        'position': currency_id.position,
                        'list_len':[a for a in range(0,report.display_detail == 'detail_with_hierarchy' and 4)],
                        'level': report.display_detail == 'detail_with_hierarchy' and 4,
                        'account_type': account.internal_type,
                    }
                    if data['debit_credit']:
                        vals['debit'] = value['debit']
                        vals['credit'] = value['credit']
                        if not account.company_id.currency_id.is_zero(vals['debit']) or not account.company_id.currency_id.is_zero(vals['credit']):
                            flag = True
                    if not account.company_id.currency_id.is_zero(vals['balance']):
                        flag = True
                    if data['enable_filter']:
                        vals['balance_cmp'] = value['comp_bal'] * report.sign
                        if not account.company_id.currency_id.is_zero(vals['balance_cmp']):
                            flag = True
                    if flag:
                        sub_lines.append(vals)
                lines += sorted(sub_lines, key=lambda sub_line: sub_line['name'])
        return lines

    @api.model
    def get_report_values(self, docids, data=None):
        data = dict({'form': data})
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        if data['form'].get('enable_filter'):
            data['form']['debit_credit'] = False

        date_from, date_to = False, False
        used_context = {}
        if data['form'].get('date_filter'):
            date_from, date_to = self.get_date_from_filter(data['form'].get('date_filter')[0])
            used_context['date_from'] = date_from
            used_context['date_to'] = date_to
            data['form']['date_from'] = date_from
            data['form']['date_to'] = date_to
        else:
            used_context['date_from'] = data['form'].get('date_from', False)
            used_context['date_to'] = data['form'].get('date_to', False)

        used_context['strict_range'] = True
        used_context['journal_ids'] = self.env['account.journal'].search([('company_id','in',data['form']['company_ids'])]).mapped('id')
        used_context['date_to'] = data['form'].get('date_to','')
        used_context['date_from'] = data['form'].get('date_from','')
        used_context['state'] = data['form'].get('target_move', '')
        data['form']['used_context'] = used_context

        comparison_context = {}
        comparison_context['strict_range'] = True
        comparison_context['journal_ids'] = self.env['account.journal'].search(
            [('company_id', 'in', data['form']['company_ids'])]).mapped('id')
        if data['form'].get('filter_cmp') == 'filter_date':
            comparison_context['date_to'] = data['form'].get('date_to_cmp', '')
            comparison_context['date_from'] = data['form'].get('date_from_cmp', '')
        else:
            comparison_context['date_to'] = False
            comparison_context['date_from'] = False
        comparison_context['state'] = data['form'].get('target_move', '')
        data['form']['comparison_context'] = comparison_context

        report_lines = self.get_account_lines(data.get('form'))
        return data, report_lines

    @api.model
    def action_view(self, docids, data=None):
        data, report_lines = self.get_report_values(docids, data)
        return json.dumps({
            'doc_model': 'accounting.report',
            'data': data['form'],
            'get_account_lines': report_lines,
        })

    @api.model
    def action_pdf(self, docids, data=None):
        data, report_lines = self.get_report_values(docids, data)
        data['form']['account_report_id'] = self.env.ref('account.account_financial_report_profitandloss0').id
        wizard = self.env['accounting.report'].create(data['form'])
        action = wizard._print_report(data)
        action['context']['active_id'] = action['context']['active_ids'][0]
        action['context']['active_model'] = 'accounting.report'
        return action

    @api.model
    def action_xlsx(self, docids, data=None):
        data, report_lines = self.get_report_values(docids, data)
        return {
            'doc_model': 'accounting.report',
            'data': data['form'],
            'lines': report_lines,
        }
