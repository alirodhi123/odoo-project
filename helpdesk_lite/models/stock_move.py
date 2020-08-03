# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2014-2016 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, fields, models

class StockMoveHelpdesk(models.Model):
    _inherit = 'stock.move'

    @api.model
    def write(self, vals):
        res = super(StockMoveHelpdesk, self).write(vals)
        from odoo import workflow
        if vals.get('state') == 'assigned':
            ticket_obj = self.env['helpdesk_lite.ticket']
            ticket_ids = ticket_obj.search([('procurement_group_id', 'in', [x.group_id.id for x in self])])
            for ticket_id in ticket_ids:
                if order_id.test_ready():
                    workflow.trg_validate(self.env.user.id, 'helpdesk_lite.ticket', ticket_id.id, 'parts_ready', self.env.cr)
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: