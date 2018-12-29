# -*- coding: utf-8 -*-

from odoo import models, fields, api


class new_object(models.Model):
    _name = 'new.object'

    nama = fields.Many2one('res.partner', required=True)
    new_object_ids = fields.One2many('new.object.detail', 'new_object_id')

    @api.multi
    def open_second_class(self):
        ac = self.env['ir.model.data'].xmlid_to_res_id('belajar_context.view_mymodule_tbl_form', raise_if_not_found=True)
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





class new_object_dus(models.Model):
    _name = 'new.object.detail'

    new_object_id = fields.Many2one('new.object')
    alamat = fields.Text(string="Alamat")
    umur = fields.Char(string="Umur")
    jk = fields.Char(string="Jenis Kelamin")

