# -*- encoding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class ProductTemplate(models.Model):
    _inherit = "product.template"

    penulis = fields.Char('Penulis')
    status_peminjaman = fields.Selection([('tersedia','Tersedia'),('belum_tersedia','Belum Tersedia'),('sedang_dipinjam','Sedang Dipinjam')], default='tersedia', 
                                         compute="_compute_status_peminjaman",string="Status Peminjaman")
    
    def _compute_status_peminjaman(self):
        for pr in self:
            for rec in self.env['account.move.line'].search([('product_id.product_tmpl_id','=',pr.id)]):
                if rec.move_id.status_peminjaman in ('dipinjam','terlambat'):
                    pr.status_peminjaman = 'sedang_dipinjam'
                else:
                    pr.status_peminjaman = 'tersedia'


