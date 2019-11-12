from odoo import models, fields, api


class SelfEvaluation(models.Model):
    _name = 'x.self.eval'
    _inherit = 'mail.thread'
    _description = 'Self Evaluaton'

    name = fields.Char()
    x_self_eval_ids = fields.One2many('x.self.eval.line', 'x_self_eval_id', string="Self Evaluation")
    x_master_se_eval = fields.Many2one('x.master.self.evaluation', string="Master Self Evaluation")
    x_periode_id = fields.Many2one('x.self.evaluation.kanban', string="Periode Bulan")
    x_employee_id = fields.Many2one('hr.employee', string="Employee")
    x_department_id = fields.Many2one('hr.department', related='x_employee_id.department_id', readonly=True,
                                      string="Department")
    x_tanggal_penilaian = fields.Date(default=fields.Datetime.now, string="Tanggal Penilaian")
    x_periode_penilaian_from = fields.Date(string="From")
    x_periode_penilaian_to = fields.Date(string="To")

    @api.model
    def create(self, vals):
        res = super(SelfEvaluation, self).create(vals)

        # Sequence
        sequence = self.env['ir.sequence'].next_by_code('sequence.x.self.evaluation') or ('New')
        res.update({'name': sequence})

        return res

    # Main Function button Generate Question
    @api.multi
    def main_function_generate_question(self):
        for self_eval in self:
            self_eval.delete_question()
            self_eval.function_get_question()

    # Function Generate Questions
    @api.multi
    def function_get_question(self):
        temp = []
        master_se_var = self.x_master_se_eval
        master_se = self.env['x.master.self.evaluation'].search([('id', '=', master_se_var.id)])

        if master_se:
            for row in master_se.x_master_se_ids:
                values = {}
                values['x_se_question'] = row.x_question

                temp.append((0, 0, values))

            return self.update({'x_self_eval_ids': temp})

    # Function delete question
    @api.multi
    def delete_question(self):
        master_self_eval = self.x_master_se_eval
        temp = []

        master_se = self.env['x.master.self.evaluation'].search([('id', '=', master_self_eval.id)])
        if master_se:
            temp.append(([5]))

            return self.update({'x_self_eval_ids': temp})

class SelfEvaluationLine(models.Model):
    _name = 'x.self.eval.line'

    x_self_eval_id = fields.Many2one('x.self.eval', ondelete='cascade')
    x_se_question = fields.Text(string="Questions")
    x_se_answer = fields.Text(string="Your Answer")
