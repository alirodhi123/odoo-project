from odoo import models, fields, api
from datetime import datetime


class ValidateAbsen(models.Model):
    _name = 'x.popup.validate'

    x_popup_validate_ids = fields.One2many('x.popup.validate.line', 'x_popup_validate_id')
    x_count_data = fields.Integer(compute='_compute_line_count', string="Employee Count")


    @api.model
    def default_get(self, fields):
        res = super(ValidateAbsen, self).default_get(fields)
        terms = []

        hr_attendance = self.env['hr.attendance']
        attendance_obj = self.env['x.attendance.attendance']
        attendance_ids = self.env.context.get('active_ids', False)

        attendance = attendance_obj.browse(attendance_ids)

        for row in attendance:
            values = {}
            id = row.id
            employee = row.x_employee_attend
            department = row.x_department_attend
            contract = row.x_contract_type_attend
            format_tanggal = row.x_to_varchar_attend
            check_in_view = row.x_check_in_view_attend
            check_out_view = row.x_check_out_view_attend
            check_in = row.x_check_in_attend
            check_out = row.x_check_out_attend
            categ_in = row.x_categ_in_attend
            categ_out = row.x_categ_out_attend
            selisih_masuk = row.x_selisih_masuk_attend
            selisih_pulang = row.x_selisih_pulang_attend
            state = row.state_attend

            values['x_attendance_attendance_id'] = id
            values['x_employee_validate'] = employee.id
            values['x_dept_validate'] = department.id
            values['x_contract_type_validate'] = contract.id
            values['x_format_tanggal_validate'] = format_tanggal
            values['x_checkin_validate_view'] = check_in_view
            values['x_checkout_validate_view'] = check_out_view
            values['x_checkin_validate'] = check_in
            values['x_checkout_validate'] = check_out
            values['x_categ_in_validate'] = categ_in
            values['x_categ_out_validate'] = categ_out
            values['x_selisih_masuk_validate'] = selisih_masuk
            values['x_selisih_pulang_validate'] = selisih_pulang
            values['x_state_validate'] = state

            terms.append((0, 0, values))
            res['x_popup_validate_ids'] = terms

        return res

    # Function menghitung jumlah employee yang akan di validate
    @api.depends('x_popup_validate_ids')
    def _compute_line_count(self):
        self.x_count_data = len(self.mapped('x_popup_validate_ids'))

    # Klik button VALIDATE
    @api.multi
    def validate_absensi(self):
        for attendance in self:
            attendance_line = attendance.x_popup_validate_ids
            hr_attendance_obj = attendance.env['hr.attendance']
            attendance_attendance_obj = attendance.env['x.attendance.attendance']

            for row in attendance_line:
                employee = row.x_employee_validate
                department = row.x_dept_validate
                contract = row.x_contract_type_validate
                format_tgl = row.x_format_tanggal_validate
                checkin = row.x_checkin_validate
                checkout = row.x_checkout_validate
                checkin_view = row.x_checkin_validate_view
                checkout_view = row.x_checkout_validate_view
                categ_in = row.x_categ_in_validate
                categ_out = row.x_categ_out_validate
                selisih_masuk = row.x_selisih_masuk_validate
                selisih_pulang = row.x_selisih_pulang_validate
                state = row.x_state_validate

                if checkin and checkout:
                    hr_attendance_obj.create({
                        'employee_id': employee.id,
                        'x_checkin_view_hr': checkin_view,
                        'x_checkout_view_hr': checkout_view,
                        'check_in': checkin,
                        'check_out': checkout,
                        'x_department_hr': department.id,
                        'x_contract_type_hr': contract.id,
                        'x_format_tanggal_hr': format_tgl,
                        'x_categ_in_hr': categ_in,
                        'x_categ_out_hr': categ_out,
                        'x_selisih_masuk_hr': selisih_masuk,
                        'x_selisih_pulang_hr': selisih_pulang,
                        'x_state_hr': 'validate'
                    })
                    pass

            attendance.update_state()

            # Menampilkan message
            result = {
                'name': 'Success',
                'view_type': 'form',
                'res_model': 'x.popup.validate.message',
                'target': 'new',
                'context': {
                    'default_name':  str(self.x_count_data) + " Absensi Data Has Been Validated...",
                },
                'type': 'ir.actions.act_window',
                'view_mode': 'form'
            }
            return result

    @api.multi
    def update_state(self):
        attendance_line = self.x_popup_validate_ids
        attendance_obj = self.env['x.attendance.attendance']

        for row in attendance_line:
            id = row.x_attendance_attendance_id.id

            validate = attendance_obj.search([('id', '=', id)])
            if validate:
                validate.write({'state_attend': 'validate'})

        return validate


class ValidateAbsenLine(models.Model):
    _name = 'x.popup.validate.line'

    x_attendance_attendance_id = fields.Many2one('x.attendance.attendance')
    x_popup_validate_id = fields.Many2one('x.popup.validate')
    x_employee_validate = fields.Many2one('hr.employee', string="Employee")
    x_dept_validate = fields.Many2one('hr.department', string="Department")
    x_contract_type_validate = fields.Many2one('hr.contract.type', string="Contract Type")
    x_format_tanggal_validate = fields.Char(string="Format Tanggal")
    x_format_tanggal = fields.Char(string="Format Tanggal")
    x_checkin_validate_view = fields.Datetime(string="Check In View")
    x_checkout_validate_view = fields.Datetime(string="Check Out View")
    x_checkin_validate = fields.Datetime(string="Check In")
    x_checkout_validate = fields.Datetime(string="Check Out")
    x_selisih_masuk_validate = fields.Char(string="Selisih Masuk")
    x_selisih_pulang_validate = fields.Char(string="Selisih Pulang")
    x_categ_in_validate = fields.Char(string="Category In")
    x_categ_out_validate = fields.Char(string="Category Out")
    x_state_validate = fields.Selection([('draft', 'Draft'), ('validate', 'Validated')], default='draft', string="Status")


class ValidateMessage(models.Model):
    _name = 'x.popup.validate.message'

    name = fields.Char()