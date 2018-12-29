# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Partner(models.Model):
    _inherit = 'res.partner'
    
    instructor = fields.Boolean("Instruktur")
    session_ids = fields.Many2many('training.sesi', string="Menghadiri Sesi", readonly=True)