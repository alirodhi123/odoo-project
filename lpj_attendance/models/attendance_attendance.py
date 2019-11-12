from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar


class x_attendance_attendance(models.Model):
    _name = 'x.attendance.attendance'

    x_contract_id = fields.Many2one('hr.contract')
    x_employee_attend = fields.Many2one('hr.employee', string="Emloyee")
    x_check_in_attend = fields.Datetime(string="Check In")
    x_check_out_attend = fields.Datetime(string="Check Out")
    x_categ_in_attend = fields.Char(string="Category In")
    x_categ_out_attend = fields.Char(string="Category Out")
    state_attend = fields.Selection([('draft', 'Draft'), ('validate', 'Validated')], default='draft')
    x_check_in_view_attend = fields.Datetime(string="Check In View")
    x_check_out_view_attend = fields.Datetime(string="Check Out View")
    x_date_attend = fields.Date(string="Date")
    x_id_attend = fields.Integer()
    x_to_varchar_attend = fields.Char(string="Format Tanggal")
    x_contract_type_attend = fields.Many2one('hr.contract.type', string="Contract Type")
    x_selisih_pulang_attend = fields.Char(string="Selisih Keluar")
    x_selisih_masuk_attend = fields.Char(string="Selisih Masuk")
    x_department_attend = fields.Many2one('hr.department', related='x_employee_attend.department_id',
                                          string="Department", readonly=True)

    @api.onchange('x_check_in_view_attend', 'x_check_out_view_attend')
    def selisih_masuk(self):
        hours = 7
        department_id = self.x_department_attend
        check_in = self.x_check_in_view_attend
        check_out = self.x_check_out_view_attend
        # Staff
        jam_masuk_staff = datetime.strptime('08:00', '%H:%M')
        jam_masuk_5 = datetime.strptime('08:30', '%H:%M')
        jam_pulang_staff = datetime.strptime('17:00', '%H:%M')

        # Produksi
        jam_masuk_prd = datetime.strptime('07:45', '%H:%M')
        jam_pulang_prd = datetime.strptime('16:00', '%H:%M')


        # CHECKIN
        if check_in != False:
            format_date_in_view = datetime.strptime(str(check_in), '%Y-%m-%d %H:%M:%S') + relativedelta(
                hours=float(hours))
            # Masukkan format date +7 ke dalam database
            self.x_check_in_attend = format_date_in_view

            # Ubah format tanggal dari 2019-08-10 menjadi 190810
            format_date = datetime.strptime(str(check_in), '%Y-%m-%d %H:%M:%S').strftime('%y%m%d')
            self.x_to_varchar_attend = format_date
            # Mecari hari dari inputan tanggal
            hari = datetime.strptime(str(check_in), '%Y-%m-%d %H:%M:%S').strftime('%A')
            # Mengitung selisih masuk
            # Jika checkin lebih cepat daripada jam masuk (early)
            if format_date_in_view.time() < jam_masuk_staff.time():
                hasil = jam_masuk_staff - format_date_in_view
                menit = (hasil.seconds) / 60
                self.x_selisih_masuk_attend = menit * -1
            # Late
            else:
                hasil = format_date_in_view - jam_masuk_staff
                menit = (hasil.seconds) / 60
                self.x_selisih_masuk_attend = menit

            # Jika employee adalah PRD
            if department_id == 9:
                if format_date_in_view.time() > jam_masuk_prd.time() and \
                    format_date_in_view.time() < datetime.strptime('08:15', '%H:%M'):
                    self.x_categ_in_attend = "Kategori 1 (dibawah 30 menit)"

                elif format_date_in_view.time() > datetime.strptime('08:15', '%H:%M').time():
                    self.x_categ_in_attend = "Kategori 2 (diatas 30)"

                elif format_date_in_view.time() < jam_masuk_prd.time():
                    self.x_categ_in_attend = "tidak telat"


            # Jika employee bukan PRD
            else:
                if hari == "Sabtu":
                    self.x_categ_in_attend = "tidak telat"

                else:
                    # Jika checkin > jam 8
                    if format_date_in_view.time() > jam_masuk_staff.time() and \
                            format_date_in_view.time() < datetime.strptime('08:30', '%H:%M').time():
                        self.x_categ_in_attend = "Kategori 1 (dibawah 30 menit)"

                    elif format_date_in_view.time() > datetime.strptime('08:30', '%H:%M').time():
                        self.x_categ_in_attend = "Kategori 2 (diatas 30)"

                    elif format_date_in_view.time() < jam_masuk_staff.time():
                        self.x_categ_in_attend = "tidak telat"

        # CHECKOUT
        if check_out != False:
            format_date_out_view = datetime.strptime(str(check_out), '%Y-%m-%d %H:%M:%S') + relativedelta(
                hours=float(hours))
            # Masukkan format date +7 ke dalam database
            self.x_check_out_attend = format_date_out_view
            # Mencari hari
            hari = datetime.strptime(str(check_out), '%Y-%m-%d %H:%M:%S').strftime('%A')
            # Mengitung selisih masuk
            # Jika checkin lebih cepat daripada jam masuk (early)
            if format_date_out_view.time() < jam_pulang_staff.time():
                selisih = jam_masuk_staff - format_date_out_view
                menit = (selisih.seconds) / 60
                self.x_selisih_pulang_attend = menit * -1
            # Late
            else:
                selisih = format_date_out_view - jam_pulang_staff
                menit = (selisih.seconds) / 60
                self.x_selisih_pulang_attend = menit

            # Jika employee adalah PRD
            if department_id == 9:
                if hari == "Sabtu":
                    if format_date_out_view.time() > datetime.strptime('13:00', '%H:%M'):
                        self.x_categ_out_attend = "Lembur"


                if format_date_out_view.time() > jam_pulang_prd.time() and \
                    format_date_out_view.time <= datetime.strptime('16:26', '%H:%M').time():
                    self.x_categ_out_attend = "PLG NORMAL"

                elif format_date_out_view.time() > datetime.strptime('16:26', '%H:%M').time():
                    self.x_categ_out_attend = "Lembur"

            # Jika employee bukan PRD
            else:
                if hari == "Sabtu":
                    self.x_categ_out_attend = "Lembur Weekend"

                else:
                    if check_out == check_in:
                        self.x_categ_out_attend = "jam kerja kurang dari 4 jam"
                    elif format_date_out_view.time() > jam_pulang_staff.time():
                        self.x_categ_out_attend = "PLG NORMAL"





