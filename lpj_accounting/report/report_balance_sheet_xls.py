from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from datetime import datetime
import time
from odoo import api, models, _
from odoo.exceptions import UserError


class BalanceSheetXls(ReportXlsx):

    def generate_xlsx_report(self, workbook, data, lines):

        # self.get_account_lines(lines)
        self.env.cr.execute("SELECT MAX(id) FROM accounting_report")
        sql_balance_sheet = self.env.cr.fetchone()
        if sql_balance_sheet:
            id_balance_sheet = sql_balance_sheet[0]

        balance_sheet_obj = self.env['accounting.report'].search([('id', '=', id_balance_sheet)])
        if balance_sheet_obj:
            for o in balance_sheet_obj:
                target_move = o.target_move
                date_from = o.date_from
                date_to = o.date_to
                display_debit_credit = o.debit_credit
                account_report = o.account_report_id.name
                journal = o.journal_ids

                # Ubah selection targer moves ke dalam string
                if target_move == "posted":
                    var_target_move = "All Posted Entries"
                else:
                    var_target_move = "All Entries"
                    pass

                if date_from and date_to:
                    self.env.cr.execute(
                        "select aa.id, aa.name, aa.code as code, afr1.name as urutan1, afr2.name as urutan2, afr3.name as urutan3, " 
                        "afr4.name as urutan4, "
                        "sum(aml.debit) as debit, "
                        "sum(aml.credit) as credit, "
                        "sum(aml.balance) as balance "
                        "from account_move am "
                        "left join account_move_line aml on am.id = aml.move_id "
                        "left join account_account aa on aml.account_id = aa.id "
                        "left join account_account_type aat on aat.id = aa.user_type_id "
                        "left join account_account_financial_report aafr on aa.id = aafr.account_id " 
                        "left join account_financial_report afr4 on aafr.report_line_id = afr4.id " 
                        "left join account_financial_report afr3 on afr3.id = afr4.parent_id "
                        "left join account_financial_report afr2 on afr2.id = afr3.parent_id "
                        "left join account_financial_report afr1 on afr1.id = afr2.parent_id "
                        "where aml.date between '2019-01-01 00:00:00' and '2019-09-30 23:59:59' " 
                            "and (afr1.name = '"+ str(account_report) +"' or afr2.name = '"+ str(account_report) +"' or afr3.name = '"+ str(account_report) +"' or afr4.name = '"+ str(account_report) +"') "
                            "and am.state = '"+ str(target_move) +"' "
                        "group by aa.name, afr1.name, aa.id,afr2.name, afr3.name, afr4.name "
                        "union all "
                        "select aa.id, aa.code as code, aa.name, afr1.name as urutan1, afr2.name as urutan2, afr3.name as urutan3, " 
                        "afr4.name as urutan4, "
                        "sum(aml.debit) as debit, "
                        "sum(aml.credit) as credit, "
                        "sum(aml.balance) as balance "
                        "from account_move am "
                        "left join account_move_line aml on am.id = aml.move_id "
                        "left join account_account aa on aml.account_id = aa.id "
                        "left join account_account_type aat on aat.id = aa.user_type_id "
                        "left join account_account_financial_report_type aafrt on aat.id = aafrt.account_type_id " 
                        "left join account_financial_report afr4 on aafrt.report_id = afr4.id "
                        "left join account_financial_report afr3 on afr3.id = afr4.parent_id "
                        "left join account_financial_report afr2 on afr2.id = afr3.parent_id "
                        "left join account_financial_report afr1 on afr1.id = afr2.parent_id "
                        "where aml.date between '2019-01-01 00:00:00' and '2019-09-30 23:59:59' " 
                            "and (afr1.name = '"+ str(account_report) +"' or afr2.name = '"+ str(account_report) +"' or afr3.name = '"+ str(account_report) +"' or afr4.name = '"+ str(account_report) +"') "
                            "and am.state = '"+ str(target_move) +"' "
                            "and aa.id not in ( "
                                "select aa.id "
                                "from account_move am "
                                "left join account_move_line aml on am.id = aml.move_id "
                                "left join account_account aa on aml.account_id = aa.id "
                                "left join account_account_type aat on aat.id = aa.user_type_id "
                                "left join account_account_financial_report aafr on aa.id = aafr.account_id "
                                "left join account_financial_report afr4 on aafr.report_line_id = afr4.id "
                                "left join account_financial_report afr3 on afr3.id = afr4.parent_id "
                                "left join account_financial_report afr2 on afr2.id = afr3.parent_id "
                                "left join account_financial_report afr1 on afr1.id = afr2.parent_id "
                                "where aml.date between '2019-01-01 00:00:00' and '2019-09-30 23:59:59' "
                                "and (afr1.name = '"+ str(account_report) +"' or afr2.name = '"+ str(account_report) +"' or afr3.name = '"+ str(account_report) +"' or afr4.name = '"+ str(account_report) +"') "
                                "and am.state = '"+ str(target_move) +"' "
                                "group by aa.id) "
                        "group by aa.name, afr1.name, aa.id,afr2.name, afr3.name, afr4.name "
                        "order by urutan4, urutan3, urutan2, urutan1"
                    )

                    sql = self.env.cr.fetchall()


        # Set format
        sheet = workbook.add_worksheet("Balance Sheet Report")
        format_judul = workbook.add_format({'font_size': 22, 'align': 'center'})
        format_header = workbook.add_format({'font_size': 12, 'bold': True, 'align': 'center'})
        format_header2 = workbook.add_format({'font_size': 12, 'bold': True})
        format_value = workbook.add_format({'font_size': 12, 'align': 'center'})
        format_left = workbook.add_format({'font_size': 12})
        format_right = workbook.add_format({'font_size': 12, 'align': 'right'})
        format_warning = workbook.add_format({'font_size': 12, 'align': 'right', 'bg_color': 'red'})
        format_urutan_pertama = workbook.add_format({'font_size': 12, 'bold': True})

        # Membuat format header
        row = 6
        column = 0
        sheet.merge_range('B1:D1', "Balance Sheet", format_judul)

        if display_debit_credit == True:

            # Set lebar kolom
            sheet.set_column('A:A', 20)
            sheet.set_column('B:B', 25)
            sheet.set_column('C:C', 25)
            sheet.set_column('D:D', 25)
            sheet.set_column('E:E', 25)

            # Set header
            sheet.write('A3', 'Target Moves', format_header2)
            sheet.write('B3', var_target_move, format_value)
            sheet.write('D3', 'Date From', format_header2)
            sheet.write('E3', date_from, format_value)
            sheet.write('D4', 'Date to', format_header2)
            sheet.write('E4', date_to, format_value)

            # Set header table
            sheet.write(row, column, 'Account', format_header)
            sheet.write(row, column + 1, 'Name', format_header)
            sheet.write(row, column + 2, 'Debit', format_header)
            sheet.write(row, column + 3, 'Credit', format_header)
            sheet.write(row, column + 4, 'Balance', format_header)

            # Isi table
            if sql:
                temp = ""
                for isi_data in sql:
                    row += 1

                    if isi_data[6] != temp:
                        temp = isi_data[6]
                        sheet.write(row, column, temp, format_urutan_pertama) # Tipe jurnal

                    sheet.write(row, column + 1, isi_data[1] + " " + isi_data[2], format_left) # Code + name
                    sheet.write(row, column + 2, isi_data[7], format_right) # Debit
                    sheet.write(row, column + 3, isi_data[8], format_right) # Credit
                    if isi_data[9] < 0: # Jika balance sheet minus
                        sheet.write(row, column + 4, isi_data[9], format_warning) # Balance minus
                    else:
                        sheet.write(row, column + 4, isi_data[9], format_right)  # Balance

                sheet.write_formula(row + 1, column + 5, '{=SUM(E8:E%s)}' % (str(row+1)), format_right)

        # Jika show debit dan credit false
        else:
            # Set lebar kolom
            sheet.set_column('A:A', 20)
            sheet.set_column('B:B', 25)
            sheet.set_column('C:C', 25)

            # Set header
            sheet.write('A3', 'Target Moves', format_header2)
            sheet.write('B3', var_target_move, format_value)
            sheet.write('D3', 'Date From', format_header2)
            sheet.write('E3', date_from, format_value)
            sheet.write('D4', 'Date to', format_header2)
            sheet.write('E4', date_to, format_value)

            # Set header table
            sheet.write(row, column, 'Name', format_header)
            sheet.write(row, column + 1, 'Balance', format_header)

            # Isi table
            if sql:
                for isi_data in sql:
                    row += 1
                    sheet.write(row, column, isi_data[6], format_urutan_pertama)  # Tipe jurnal
                    sheet.write(row, column, isi_data[1] + " " + isi_data[2], format_left) # Code + name
                    if isi_data[9] < 0:
                        sheet.write(row, column + 1, isi_data[9], format_warning)  # Balance minus
                    else:
                        sheet.write(row, column + 1, isi_data[9], format_right)  # Balance

BalanceSheetXls('report.lpj_accounting.balance_sheet_report.xlsx', 'account.financial.report')

