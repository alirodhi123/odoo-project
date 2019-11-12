from odoo import models, fields, api


class GaolSetting(models.Model):
    _name = 'x.goal.setting'
    _inherit = 'mail.thread'
    _description = 'Goal Setting'

    def _default_employee(self):
        return self.env.context.get('default_x_employee_id') or self.env['hr.employee'].search(
            [('user_id', '=', self.env.uid)], limit=1)

    name = fields.Char()
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed')], default='draft', track_visibility="onchange")
    x_goal_setting_ids = fields.One2many('x.goal.setting.line', 'x_goal_setting_id')
    x_employee_id = fields.Many2one('hr.employee', required=True, string="Nama Penilai",
                                    track_visibility="onchange", default=_default_employee)
    x_department_id = fields.Many2one('hr.department', related='x_employee_id.department_id', readonly=True,
                                      string="Department", track_visibility="onchange")
    x_job_id = fields.Many2one('hr.job', related='x_employee_id.job_id', readonly=True,
                               string="Jabatan", track_visibility="onchange")
    x_nama_karyawan = fields.Many2one('hr.employee', string="Nama Karyawan", required=True, track_visibility="onchange")
    x_job_id_karyawan = fields.Many2one('hr.job', related='x_nama_karyawan.job_id', readonly=True,
                                        string="Jabatan", track_visibility="onchange")
    comment = fields.Text()
    user_id = fields.Many2one('res.users', string='User', related='x_employee_id.user_id', related_sudo=True,
                              default=lambda self: self.env.uid, readonly=True, track_visibility="onchange")
    x_periode_id = fields.Many2one('x.goal.setting.kanban', required=True, string="Periode Bulan",
                                   track_visibility="onchange")
    # FOOTER
    x_total_bobot = fields.Float(string="Total Bobot", compute='compute_value')
    x_total_target = fields.Float(string="Total Target", compute='compute_value')
    x_total_pencapaian = fields.Float(string="Total Pencapaian", compute='compute_value')
    x_total_nilai = fields.Float(string="Total Nilai", compute='compute_value')


    @api.model
    def create(self, vals):
        res = super(GaolSetting, self).create(vals)

        # Sequence
        sequence = self.env['ir.sequence'].next_by_code('sequence.x.goal.setting') or ('New')
        res.update({'name': sequence})

        return res


    # Method menghitung TOTAL bobot, target, pencapaian
    @api.depends('x_goal_setting_ids.x_bobot', 'x_goal_setting_ids.x_target',
                 'x_goal_setting_ids.x_pencapaian', 'x_goal_setting_ids.x_nilai')
    def compute_value(self):
        line_count = len(self.mapped('x_goal_setting_ids'))
        bobot = 0
        target = 0
        pencapaian = 0
        nilai = 0

        for row in self.x_goal_setting_ids:
            bobot = bobot + row.x_bobot
            target = target + row.x_target
            pencapaian = pencapaian + row.x_pencapaian
            nilai = nilai + row.x_nilai

        if line_count != 0:
            self.x_total_bobot = bobot
            self.x_total_target = target / line_count
            self.x_total_pencapaian = pencapaian / line_count
            self.x_total_nilai = nilai


class GoalSettingLine(models.Model):
    _name = 'x.goal.setting.line'

    x_goal_setting_id = fields.Many2one('x.goal.setting', ondelete='cascade')
    x_program_kerja = fields.Text(string="Program Kerja")
    x_indikator = fields.Text(string="Indikator yang Diharapkan")
    x_pemberi_gs = fields.Text(string="Yang Memberikan")
    x_real_value = fields.Text(string="Real Action")
    x_bobot = fields.Float(string="Bobot")
    x_target = fields.Float(string="Target(%)")
    x_pencapaian = fields.Float(string="Pencapaian(%)")
    x_nilai = fields.Float(string="Nilai", compute='compute_nilai')
    x_action_plan = fields.Text(string="Action Plan")


    # GOAL SETTING
    # Method menghitung nilai dari rumus excel
    @api.depends('x_bobot', 'x_target', 'x_pencapaian')
    def compute_nilai(self):
        for row in self:
            bobot = row.x_bobot
            target = row.x_target
            pencapaian = row.x_pencapaian

            if target != 0:
                nilai_akhir = float(pencapaian / target) * bobot
                row.x_nilai = nilai_akhir



