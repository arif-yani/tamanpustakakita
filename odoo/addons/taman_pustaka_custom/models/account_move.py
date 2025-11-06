from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from urllib.parse import quote
from datetime import date, timedelta

class AccountMove(models.Model):
    _inherit = "account.move"

    status_peminjaman = fields.Selection([('draft','Draft'),('dipinjam','Dipinjam'),('dikembalikan','Dikembalikan'),('terlambat','Terlambat')],
                                        default='draft',string='Status Peminjaman') 
    waktu_pengembalian = fields.Date(string="Waktu Pengembalian")

    @api.onchange('invoice_date')
    def onchange_invoice_date(self):
        for rec in self:
            if rec.invoice_date:
                rec.waktu_pengembalian = rec.invoice_date + timedelta(days=7)

    def action_post(self):
        res = super(AccountMove, self).action_post()
        self.status_peminjaman = 'dipinjam'

    def action_set_dikembalikan(self):
        self.status_peminjaman = 'dikembalikan'
        