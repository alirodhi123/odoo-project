
from odoo import models, fields, api

class Wizard(models.TransientModel):
    _name = 'training.wizard'

    def _default_sesi(self):
        return self.env['training.sesi'].browse(self._context.get('active_id'))
    
    session_id = fields.Many2one('training.sesi', string="Sesi", default=_default_sesi)
    attendee_ids = fields.Many2many('res.partner', string="Peserta")

    session_ids = fields.Many2many('training.sesi', string="Sesi")
    
    @api.multi
    def tambah_peserta(self):
        self.session_id.attendee_ids |= self.attendee_ids
        return {}
    
    
    @api.multi
    def tambah_banyak_peserta(self):
        for sesi in self.session_ids:
            sesi.attendee_ids |= self.attendee_ids
        return {}
