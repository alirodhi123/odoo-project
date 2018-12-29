# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TestModel1(models.Model):
    _name = 'test.model'

    def _default_mrp_production(self):
        return self.env['new.object'].browse(self._context.get('active_id'))

    x_no_new = fields.Many2one('new.object', string="New object", default=_default_mrp_production)
    code = fields.Many2one('res.partner')
    description = fields.Char('Description')
    test_model_ids = fields.One2many('test.model2', 'test_model_id')

    @api.model
    def create(self, vals):
        res = super(TestModel1, self).create(vals)

        id = vals['x_no_new']
        terms_obj = self.env['new.object']
        terms = []
        termsids = terms_obj.search([('id', '=', id)])
        for rec in termsids.new_object_ids:
            values = {}
            values['employee'] = rec.alamat
            values['code_parsing'] = rec.umur
            values['desc_parsing'] = rec.jk
            terms.append((0, 0, values))

        res.update({'test_model_ids': terms})
        return res


    @api.multi
    def open_second_class(self):
        ac = self.env['ir.model.data'].xmlid_to_res_id('belajar_context.new_object_view', raise_if_not_found=True)
        TestModel1 = False

        result = {
            'name': '2nd class',
            'view_type': 'form',
            'res_model': 'test.model2',
            'view_id': ac,
            'context': {},
            'type': 'ir.actions.act_window',
            'view_mode': 'form'
        }
        return result


class TestModel2(models.Model):
    _name = 'test.model2'
    _inherits = {'test.model': 'test_model_id'}

    test_model_id = fields.Many2one('test.model')
    employee = fields.Char('ID')
    code_parsing = fields.Char(string="Code")
    desc_parsing = fields.Text(string="Description")

