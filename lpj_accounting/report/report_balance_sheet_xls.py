from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from datetime import datetime

class BalanceSheetXls(ReportXlsx):

    def generate_xlsx_report(self, workbook, data, Lines):

        sheet = workbook.add_worksheet("Balance Sheet Report")
        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 10)
        sheet.set_column('C:C', 25)
        sheet.set_column('D:D', 15)
        sheet.set_column('E:E', 10)
        sheet.set_column('F:F', 20)
        sheet.set_column('G:G', 25)
        sheet.set_column('H:H', 20)
        sheet.set_column('I:I', 20)


BalanceSheetXls('report.lpj_accounting.balance_sheet_report.xlsx', 'accounting.report')