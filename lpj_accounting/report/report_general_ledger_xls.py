from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from datetime import datetime

class GeneralLedgerXls(ReportXlsx):

    def generate_xlsx_report(self, workbook, data, Lines):

        # Mengambil id maksimal pada general ledger
        self.env.cr.execute("SELECT MAX(id) FROM account_report_general_ledger")
        sql_general_ledger = self.env.cr.fetchone()
        if sql_general_ledger:
            id_ledger = sql_general_ledger[0]

        # Mengambil semua variable general ledger
        general_ledger_obj = self.env['account.report.general.ledger'].search([('id', '=', id_ledger)])
        if general_ledger_obj:
            for o in general_ledger_obj:
                target_move = o.target_move
                sort_by = o.sortby
                display_account = o.display_account
                start_date = o.date_from
                end_date = o.date_to

                # Ubah selection targer moves ke dalam string
                if target_move == "poster":
                    var_target_move = "All Posted Entries"
                else:
                    var_target_move = "All Entries"
                    pass

                # Ubah selection sort by ke dalam string
                if sort_by == "sort_date":
                    var_sort_by = "Date"
                else:
                    var_sort_by = "Journal & Partner"
                    pass

                if display_account == "all":
                    var_display_account = "All"
                elif display_account == "movements":
                    var_display_account = "With movements"
                else:
                    var_display_account = "With balance is not equal to 0"
                    pass

                if start_date:
                    # SQL query general ledger
                    self.env.cr.execute("SELECT l.id AS lid, l.account_id AS account_id, l.date AS ldate, j.code AS lcode, " 
                                        "l.currency_id, l.amount_currency, l.ref AS lref, l.name AS lname, "
                                        "COALESCE(l.debit,0) AS debit, COALESCE(l.credit,0) AS credit, "
                                        "COALESCE(SUM(l.debit),0) - COALESCE(SUM(l.credit), 0) AS balance, m.name AS move_name, " 
                                        "c.symbol AS currency_code, p.name AS partner_name "
                                        "FROM account_move_line l "
                                        "JOIN account_move m ON (l.move_id=m.id) "
                                        "LEFT JOIN res_currency c ON (l.currency_id=c.id) "
                                        "LEFT JOIN res_partner p ON (l.partner_id=p.id) "
                                        "JOIN account_journal j ON (l.journal_id=j.id) "
                                        "JOIN account_account acc ON (l.account_id = acc.id) " 
                                        "WHERE l.date BETWEEN '"+ start_date +"' AND '"+ end_date +"'"
                                        "GROUP BY l.id, l.account_id, l.date, j.code, l.currency_id, l.amount_currency, l.ref, " 
                                        "l.name, m.name, c.symbol, p.name " 
                                        "ORDER BY l.date ASC")
                    sql = self.env.cr.fetchall()
                    # if sql:
                        # date = sql[2]
                        # journal = sql[3]
                        # currency = sql[4]
                        # amount_currency = sql[5]
                        # ref = sql[6]
                        # name = sql[7]
                        # debit = sql[8]
                        # credit = sql[9]
                        # balance = sql[10]
                        # move_name = sql[11]
                        # currency_code = sql[12]
                        # partner_name = sql[13]

            sheet = workbook.add_worksheet("General Ledger Report")
            format_judul = workbook.add_format({'font_size': 22, 'align': 'center'})
            format_header = workbook.add_format({'font_size': 12, 'bold': True, 'align': 'center'})
            format_header2 = workbook.add_format({'font_size': 12, 'bold': True})
            format_value = workbook.add_format({'font_size': 12, 'align': 'center'})
            format_left = workbook.add_format({'font_size': 12})
            format_right = workbook.add_format({'font_size': 12, 'align': 'right'})
            format_warning = workbook.add_format({'font_size': 12, 'bg_color': 'red'})

            # Membuat format header
            row = 6
            column = 0
            sheet.merge_range('D1:G1', "General Ledger", format_judul)

            # Set lebar kolom
            sheet.set_column('A:A', 20)
            sheet.set_column('B:B', 10)
            sheet.set_column('C:C', 25)
            sheet.set_column('D:D', 15)
            sheet.set_column('E:E', 10)
            sheet.set_column('F:F', 20)
            sheet.set_column('G:G', 25)
            sheet.set_column('H:H', 20)
            sheet.set_column('I:I', 20)

            # Set header
            sheet.write('A3', 'Target Moves', format_header2)
            sheet.write('B3', var_target_move, format_value)
            sheet.write('A4', 'Sorted By', format_header2)
            sheet.write('B4', var_sort_by, format_value)
            sheet.write('D3', 'Display Account', format_header2)
            sheet.write('E3', var_display_account, format_value)
            sheet.write('G3', 'Date From', format_header2)
            sheet.write('H3', start_date, format_value)
            sheet.write('G4', 'Date to', format_header2)
            sheet.write('H4', end_date, format_value)

            # Set header table (row ke berapa, kolom ke berapa, judul header, format header)
            sheet.write(row, column, 'Date', format_header)
            sheet.write(row, column + 1, 'Journal', format_header)
            sheet.write(row, column + 2, 'Partner', format_header)
            sheet.write(row, column + 3, 'Ref', format_header)
            sheet.write(row, column + 4, 'Move', format_header)
            sheet.write(row, column + 5, 'Entry Label', format_header)
            sheet.write(row, column + 6, 'Debit', format_header)
            sheet.write(row, column + 7, 'Credit', format_header)
            sheet.write(row, column + 8, 'Balance', format_header)

            # Isi table
            if sql:
                for isi_data in sql:
                    row += 1
                    sheet.write(row, column, isi_data[2], format_value) # Tanggal
                    sheet.write(row, column + 1, isi_data[3], format_value) # Journal
                    sheet.write(row, column + 2, isi_data[13], format_left) # Partner
                    sheet.write(row, column + 3, isi_data[6], format_value) # Ref
                    sheet.write(row, column + 4, isi_data[11], format_value) # Move
                    sheet.write(row, column + 5, isi_data[7], format_left) # Entry Label
                    sheet.write(row, column + 6, isi_data[8], format_right) # Debit
                    sheet.write(row, column + 7, isi_data[9], format_right) # Credit
                    if isi_data[10] < 0:
                        sheet.write(row, column + 8, isi_data[10], format_warning) # Balance
                    else:
                        sheet.write(row, column + 8, isi_data[10], format_right)  # Balance



GeneralLedgerXls('report.lpj_accounting.general_ledger_report.xlsx', 'account.invoice')