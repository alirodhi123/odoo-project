# -*- coding: utf-8 -*-

import time
from openerp import api, fields, models, _
import json
from datetime import datetime, timedelta, date
import calendar
from dateutil.relativedelta import relativedelta
from openerp.tools.misc import formatLang

class ReportGeneralLedger(models.AbstractModel):
    _inherit = 'report.account.report_generalledger'

    def _get_account_move_entry(self, accounts, init_balance, sortby, display_account):
        account_id_list = self.env.context.get('account_ids',[])
        if account_id_list:
            accounts = self.env['account.account'].browse(account_id_list)
        return super(ReportGeneralLedger,self)._get_account_move_entry(accounts, init_balance, sortby, display_account)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def _query_get(self, domain=None):
        if domain is None:
            domain = []
        if self._context.get('analytic_acc_ids', []):
            domain.append(('analytic_account_id.id', 'in',self._context.get('analytic_acc_ids', [])))
        if self._context.get('acc_tags', []):
            domain.append(('account_id.tag_ids', 'in',self._context.get('acc_tags', [])))
        if self._context.get('partner_ids', []):
            domain.append(('partner_id', 'in',self._context.get('partner_ids', [])))
        return super(AccountMoveLine,self)._query_get(domain)

class ReportDynamicGeneralLedger(models.AbstractModel):
    _name = 'report.account.dynamic.report_generalledger'

    @api.model
    def get_invoice_details(self,lref):
        '''
        Used to find out invoice id from reference number in move line
        :param lref: Char .from account move line
        :return: Integer .invoice id or False
        '''
        if lref:
            invoice_id = self.env['account.invoice'].search([('number','=',lref)])[0].id
            return invoice_id or False
        return False

    @api.multi
    def get_date_from_filter(self,filter):
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
                date_from = (day_today - timedelta(days=date.weekday()) ).strftime("%Y-%m-%d")
                date_to = (day_today + timedelta(days=6)).strftime("%Y-%m-%d")
                return date_from, date_to
            if filter['id'] == 'this_month':
                date_from = datetime(date.year, date.month, 1).strftime("%Y-%m-%d")
                date_to = datetime(date.year, date.month, calendar.mdays[date.month]).strftime("%Y-%m-%d")
                return date_from,date_to
            if filter['id'] == 'this_quarter':
                if int((date.month-1) / 3) == 0: # First quarter
                    date_from = datetime(date.year, 1, 1).strftime("%Y-%m-%d")
                    date_to = datetime(date.year, 3, calendar.mdays[3]).strftime("%Y-%m-%d")
                if int((date.month-1) / 3) == 1: # First quarter
                    date_from = datetime(date.year, 4, 1).strftime("%Y-%m-%d")
                    date_to = datetime(date.year, 6, calendar.mdays[6]).strftime("%Y-%m-%d")
                if int((date.month-1) / 3) == 2: # First quarter
                    date_from = datetime(date.year, 7, 1).strftime("%Y-%m-%d")
                    date_to = datetime(date.year, 9, calendar.mdays[9]).strftime("%Y-%m-%d")
                if int((date.month-1) / 3) == 3: # First quarter
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
                if int((date.month-1) / 3) == 0:  # First quarter
                    date_from = datetime(date.year, 1, 1).strftime("%Y-%m-%d")
                    date_to = datetime(date.year, 3, calendar.mdays[3]).strftime("%Y-%m-%d")
                if int((date.month-1) / 3) == 1:  # Second quarter
                    date_from = datetime(date.year, 4, 1).strftime("%Y-%m-%d")
                    date_to = datetime(date.year, 6, calendar.mdays[6]).strftime("%Y-%m-%d")
                if int((date.month-1) / 3) == 2:  # Third quarter
                    date_from = datetime(date.year, 7, 1).strftime("%Y-%m-%d")
                    date_to = datetime(date.year, 9, calendar.mdays[9]).strftime("%Y-%m-%d")
                if int((date.month-1) / 3) == 3:  # Fourth quarter
                    date_from = datetime(date.year, 10, 1).strftime("%Y-%m-%d")
                    date_to = datetime(date.year, 12, calendar.mdays[12]).strftime("%Y-%m-%d")
                return date_from, date_to
            date = (datetime.now() - relativedelta(years=1))
            if filter['id'] == 'last_financial_year':
                date_from = datetime(date.year, 1, 1).strftime("%Y-%m-%d")
                date_to = datetime(date.year, 12, 31).strftime("%Y-%m-%d")
                return date_from, date_to

    def _get_account_move_entry(self, accounts, init_balance, sortby, display_account):
        """
        :param:
                accounts: the recordset of accounts
                init_balance: boolean value of initial_balance
                sortby: sorting by date or partner and journal
                display_account: type of account(receivable, payable and both)

        Returns a dictionary of accounts with following key and value {
                'code': account code,
                'name': account name,
                'debit': sum of total debit amount,
                'credit': sum of total credit amount,
                'balance': total balance,
                'amount_currency': sum of amount_currency,
                'move_lines': list of move line
        }
        """
        context = dict(self.env.context or {})
        cr = self.env.cr
        MoveLine = self.env['account.move.line']
        move_lines = dict(map(lambda x: (x, []), accounts.ids))

        # Prepare initial sql query and Get the initial move lines
        if init_balance:
            init_tables, init_where_clause, init_where_params = MoveLine.with_context(context)._query_get()
            init_wheres = [""]
            if init_where_clause.strip():
                init_wheres.append(init_where_clause.strip())
            init_filters = " AND ".join(init_wheres)
            filters = init_filters.replace('account_move_line__move_id', 'm').replace('account_move_line', 'l')
            sql = ("""SELECT 0 AS lid, l.account_id AS account_id, '' AS ldate, '' AS lcode, NULL AS amount_currency, '' AS lref, 'Initial Balance' AS lname, COALESCE(SUM(l.debit),0.0) AS debit, COALESCE(SUM(l.credit),0.0) AS credit, COALESCE(SUM(l.debit),0) - COALESCE(SUM(l.credit), 0) as balance, '' AS lpartner_id,\
                '' AS move_name, '' AS mmove_id, '' AS currency_code, l.reconciled AS reconciled,\
                NULL AS currency_id,\
                '' AS invoice_id, '' AS invoice_type, '' AS invoice_number,\
                '' AS partner_name\
                FROM account_move_line l\
                LEFT JOIN account_move m ON (l.move_id=m.id)\
                LEFT JOIN res_currency c ON (l.currency_id=c.id)\
                LEFT JOIN res_partner p ON (l.partner_id=p.id)\
                LEFT JOIN account_invoice i ON (m.id =i.move_id)\
                JOIN account_journal j ON (l.journal_id=j.id)\
                WHERE l.account_id IN %s""" + filters + ' GROUP BY l.account_id,l.reconciled')
            params = (tuple(accounts.ids),) + tuple(init_where_params)
            cr.execute(sql, params)
            for row in cr.dictfetchall():
                move_lines[row.pop('account_id')].append(row)

        sql_sort = 'l.date, l.move_id'
        if sortby == 'sort_journal_partner':
            sql_sort = 'j.code, p.name, l.move_id'

        # Prepare sql query base on selected parameters from wizard
        context.update({'initial_bal':False})
        tables, where_clause, where_params = MoveLine.with_context(context)._query_get()
        wheres = [""]
        if where_clause.strip():
            wheres.append(where_clause.strip())
        filters = " AND ".join(wheres)
        filters = filters.replace('account_move_line__move_id', 'm').replace('account_move_line', 'l')

        # Get move lines base on sql query and Calculate the total balance of move lines
        sql = ('''SELECT l.id AS lid, l.account_id AS account_id, l.date AS ldate, j.code AS lcode, l.currency_id, l.amount_currency, l.ref AS lref, l.name AS lname, COALESCE(l.debit,0) AS debit, COALESCE(l.credit,0) AS credit, COALESCE(SUM(l.debit),0) - COALESCE(SUM(l.credit), 0) AS balance,\
            m.name AS move_name, l.move_id AS move_id, c.symbol AS currency_code,c.position AS amount_currency_position, p.name AS partner_name, l.reconciled AS reconciled\
            FROM account_move_line l\
            JOIN account_move m ON (l.move_id=m.id)\
            LEFT JOIN res_currency c ON (l.currency_id=c.id)\
            LEFT JOIN res_partner p ON (l.partner_id=p.id)\
            JOIN account_journal j ON (l.journal_id=j.id)\
            JOIN account_account acc ON (l.account_id = acc.id) \
            WHERE l.account_id IN %s ''' + filters + ''' GROUP BY l.id, l.account_id, l.date, j.code, l.currency_id, l.amount_currency, l.ref, l.name, m.name, c.symbol,c.position, p.name ORDER BY ''' + sql_sort)
        params = (tuple(accounts.ids),) + tuple(where_params)
        cr.execute(sql, params)

        for row in cr.dictfetchall():
            balance = 0
            if row.get('currency_id', False):
                row['amount_currency_precision'] = self.env['res.currency'].browse(int(row['currency_id'])). \
                    decimal_places
            for line in move_lines.get(row['account_id']):
                balance += line['debit'] - line['credit']
            row['balance'] += balance
            move_lines[row.pop('account_id')].append(row)

        # Calculate the debit, credit and balance for Accounts
        account_res = []
        digits = str(self.env.user.company_id.currency_id.decimal_places)
        for account in accounts:
            currency = account.currency_id and account.currency_id or account.company_id.currency_id
            res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance'])
            res['code'] = account.code
            res['name'] = account.name
            res['move_lines'] = move_lines[account.id]
            res['precision'] = digits
            for line in res.get('move_lines'):
                res['debit'] += line['debit']
                res['credit'] += line['credit']
                res['balance'] = line['balance']
                res['precision'] = digits
                res['currency_symbol'] = currency.symbol # base currency symbol
                res['currency_position'] = currency.position # base currency position
            if display_account == 'all':
                account_res.append(res)
            if display_account == 'movement' and res.get('move_lines'):
                account_res.append(res)
            if display_account == 'not_zero' and not currency.is_zero(res['balance']):
                account_res.append(res)

        return account_res

    @api.model
    def render_html(self, docids, act_type='show'):
        context = dict(self.env.context or {})
        init_balance = docids.get('initial_balance', False)
        target_moves = 'all_posted'
        if docids.get('all_posted'):
            target_moves = 'posted'
        if docids.get('all_entries'):
            target_moves = 'all'

        if docids.get('by_date'):
            sort_by = 'sort_date'
        if docids.get('by_journal_and_partner'):
            sort_by = 'sort_journal_partner'

        if docids.get('all_datas'):
            display_account = 'all'
        if docids.get('all_movements'):
            display_account = 'movement'
        if docids.get('all_balance_not_zero'):
            display_account = 'not_zero'

        codes = []
        if docids.get('journal_ids', False):
            codes = [journal.code for journal in self.env['account.journal'].search([('id', 'in', docids['journal_ids'])])]
        accounts = self.env['account.account'].search([])
        local_ctx = {
            'state':target_moves or False,
            'journal_ids':docids.get('journal_ids',[]),
            'company_ids': docids.get('company_ids', []),
            'initial_bal': docids.get('initial_balance', False),
            'strict_range':True, # Always expect date from and date_to
            'all_accounts': True,
            'display_account':display_account,
            'sort_by':sort_by
        }

        # If accounts selected
        if docids.get('account_ids', []):
            accounts = self.env['account.account'].browse(docids.get('account_ids')) or []
            local_ctx['all_accounts'] = False
        local_ctx['account_ids'] = accounts.mapped('id')
        if not local_ctx['all_accounts']:
            local_ctx['account_name'] = accounts.mapped('name')

        # If accounts tag selected
        account_tags = []
        if docids.get('account_tag_ids', []):
            account_tags = self.env['account.account.tag'].browse(docids.get('account_tag_ids')) or []
            local_ctx['acc_tags'] = account_tags.mapped('id')
            local_ctx['acc_tags_name'] = account_tags.mapped('name')

        # If partners selected
        if docids.get('partner_ids', []):
            partners = self.env['res.partner'].browse(docids.get('partner_ids')) or []
            local_ctx['partner_ids'] = partners.mapped('id')
            local_ctx['partner_name'] = partners.mapped('name')

        # If analytic account selected
        analytic_account = []
        if docids.get('analytic_account_ids', []):
            analytic_account = self.env['account.analytic.account'].browse(docids.get('analytic_account_ids')) or []
            local_ctx['analytic_acc_ids'] = analytic_account.mapped('id')
            local_ctx['analytic_acc_name'] = analytic_account.mapped('name')

        # If analytic account tags selected
        analytic_account_tags = []
        if docids.get('analytic_tag_ids', []):
            analytic_account_tags = self.env['account.analytic.tag'].browse(docids.get('analytic_tag_ids')) or []
        local_ctx['analytic_acc_tag_ids'] = analytic_account_tags

        date_from, date_to = False, False
        if docids.get('date_filter'):
            date_from, date_to = self.get_date_from_filter(docids.get('date_filter')[0])
            local_ctx['date_from'] = date_from
            local_ctx['date_to'] = date_to
        else:
            local_ctx['date_from'] = docids.get('date_from', False)
            local_ctx['date_to'] = docids.get('date_to', False)

        if act_type == 'show':
            move_lines = self.with_context(local_ctx)._get_account_move_entry(accounts, init_balance, sort_by, display_account)
            docs = self.env.context
            docargs = {
                'doc_ids': docids,
                'time': datetime.now().strftime("%Y-%m-%d"),
                'Accounts': move_lines,
                'print_journal': codes,
                'local_ctx':local_ctx
            }

            # Prepare JSON
            return json.dumps(docargs)

        if act_type == 'pdf':
            # Prepare pdf
            result = {'model': 'ir.ui.menu',
                 'ids': [],
                 'form': {'initial_balance': local_ctx['initial_bal'] or False,
                          'display_account': display_account,
                          'date_from': local_ctx['date_from'] or False,
                          'journal_ids': local_ctx.get('journal_ids',[]),
                          'used_context': local_ctx,
                          'sortby': sort_by,
                          'date_to': local_ctx['date_to'] or False,
                          'target_move': target_moves
                          }}
            if local_ctx['initial_bal']:
                result['form']['used_context'].update({'date_to':False})
                result['form']['used_context'].update({'initial_bal': False})
            return result

        if act_type == 'xlsx':
            move_lines = self.with_context(local_ctx)._get_account_move_entry(accounts, init_balance, sort_by,
                                                                              display_account)
            docargs = {
                'doc_ids': docids,
                'time': datetime.now().strftime("%Y-%m-%d"),
                'Accounts': move_lines,
                'print_journal': codes,
                'form':{'initial_balance': local_ctx['initial_bal'] or False,
                          'display_account': display_account,
                          'date_from': local_ctx['date_from'] or False,
                          'journal_ids': local_ctx.get('journal_ids',[]),
                          'partner_ids': local_ctx.get('partner_ids', []),
                          'sortby': sort_by,
                          'date_to': local_ctx['date_to'] or False,
                          'target_move': target_moves,
                          'all_accounts': local_ctx['all_accounts'],
                          'account_ids': local_ctx.get('account_ids',[]),
                          'account_tag_ids': local_ctx.get('acc_tags',[]),
                          'analytic_account_ids': local_ctx.get('analytic_acc_ids',[])
                          }
            }
            return docargs





