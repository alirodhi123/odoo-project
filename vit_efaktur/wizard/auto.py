from odoo import api, fields, models, _
from odoo.exceptions import UserError

class efaktur_wizard(models.TransientModel):
    _name = 'vit.efaktur_auto'
    
    start   = fields.Date("Invoice Date Start",required=True)
    end     = fields.Date("Invoice Date End",required=True)
    invoice_ids = fields.Many2many(comodel_name="account.invoice", string="Invoices", )

    @api.multi
    def confirm_button(self):

        invoice_ids = self.invoice_ids

        efaktur_ids = self.env['vit.efaktur'].search([('is_used','=',False)],
                                                     order="name asc")
        efaktur_len = len(efaktur_ids)

        i = 0
        for inv in invoice_ids:
            if i < efaktur_len:
                inv.efaktur_id = efaktur_ids[i]
            else:
                break
            i+=1

        self.env.cr.commit()
        raise UserError("Selesai penomoran E-Faktur %s invoices(s)!" % i)

    @api.multi
    def find_invoices(self):
        start = self.start
        end = self.end

        inv_obj = self.env['account.invoice']
        invoices = inv_obj.search([('date_invoice','>=', start),
                                   ('date_invoice','<=', end),
                                   ('state','=','open'),
                                   ('efaktur_id','=',False),
                                   ('type','=','out_invoice')
                                   ])
        i = 0
        invoice_ids = []
        for inv in invoices:
            invoice_ids.append((4,inv.id))
            i+=1

        self.invoice_ids=invoice_ids
        self.env.cr.commit()
        raise UserError("Found %s invoices(s)!" % i)

