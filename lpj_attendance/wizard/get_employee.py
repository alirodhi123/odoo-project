from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta


class WizardAbsensi(models.Model):
    _name = 'x.popup.get.employee'

    x_date_start = fields.Date(string="Date Start")
    x_date_end = fields.Date(string="Date End")


    @api.multi
    def get_employee_not_here(self):
        for attendance in self:
            hours = 7
            date_start = attendance.x_date_start
            date_end = attendance.x_date_end

            attendance_obj = attendance.env['x.attendance.attendance']
            contract_obj = attendance.env['hr.contract']
            department_obj = attendance.env['hr.department']

            if date_start and date_end:
                # format_date_in = datetime.strptime(str(date_start), '%Y-%m-%d %H:%M:%S') + relativedelta(hours=float(hours))
                # format_date_out = datetime.strptime(str(date_end), '%Y-%m-%d %H:%M:%S') + relativedelta(hours=float(hours))

                attendance.env.cr.execute("SELECT attend.id as id_x_attend, he.id as employee, attend.x_checkin as checkin, "
                                          "attend.x_checkout as checkout, attend.x_categ_in as categ_in, "
                                          "attend.x_categ_out as categ_out, to_char(attend.x_checkin, 'YYMMDD'), "
                                          "attend.x_selisih_masuk, attend.x_selisih_pulang, he.department_id "
                                          "FROM hr_employee he "
                                          "LEFT JOIN x_attendance attend ON attend.x_employee = he.id AND attend.x_checkin IN ("
                                              "SELECT attend2.x_checkin FROM x_attendance attend2 "
                                              "WHERE attend2.x_checkin BETWEEN '"+ str(date_start) +"' AND date '"+ str(date_end) +"' + time '"+ '23:59' +"')"
                                          "LEFT JOIN x_attendance_attendance xaa on xaa.x_check_in_attend = attend.x_checkin "
                                          "WHERE xaa.x_check_in_attend is null and he.x_resign_date is null")
                var = attendance.env.cr.fetchall()
                if var:
                    for row in var:
                        id = row[0]
                        employee_id = row[1]
                        checkin_checkin = row[2]
                        checkout_checkout = row[3]
                        categ_in = row[4]
                        categ_out = row[5]
                        to_varchar = row[6]
                        selisih_masuk = row[7]
                        selisih_pulang = row[8]
                        department_id = row[9]

                        # Mengambil contract type dan department dari setiap employee
                        if employee_id:
                            contract = contract_obj.search([('employee_id', '=', employee_id)])
                            department = department_obj.search([('id', '=', department_id)])

                            # Mengambil contract type
                            if contract:
                                for line in contract:
                                    contract_type = line.type_id.name
                                    pass
                            else:
                                contract_type = "Null"

                            # Mengambil nama department
                            if department:
                                for line_dept in department:
                                    department_name = line_dept.name
                                    pass
                            else:
                                department_name = "Null"

                        if checkin_checkin and checkout_checkout:
                            # Minus 7 untuk view di odoo
                            format_date_in_view = datetime.strptime(str(checkin_checkin), '%Y-%m-%d %H:%M:%S') - relativedelta(hours=float(hours))
                            format_date_out_view = datetime.strptime(str(checkout_checkout), '%Y-%m-%d %H:%M:%S') - relativedelta(hours=float(hours))

                            attendance_obj.create({
                                'x_id_attend': id,
                                'x_employee_attend': employee_id,
                                'x_contract_type_attend': contract_type,
                                'x_check_in_attend': checkin_checkin,
                                'x_check_out_attend': checkout_checkout,
                                'x_check_in_view_attend': format_date_in_view,
                                'x_check_out_view_attend': format_date_out_view,
                                'x_categ_in_attend': categ_in,
                                'x_categ_out_attend': categ_out,
                                'x_to_varchar_attend': to_varchar,
                                'x_selisih_masuk_attend': selisih_masuk,
                                'x_selisih_pulang_attend': selisih_pulang,
                                'x_department_attend': department_name
                            })
                        else:
                            attendance_obj.create({
                                'x_id_attend': id,
                                'x_employee_attend': employee_id,
                                'x_contract_type_attend': contract_type,
                                'x_categ_in_attend': categ_in,
                                'x_categ_out_attend': categ_out,
                                'x_to_varchar_attend': to_varchar,
                                'x_department_attend': department_name
                            })
                            pass


