from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
import time
from datetime import datetime, timedelta

class sale_order(models.Model):
    _inherit = "sale.order"

    is_keep_order =  fields.Boolean('Keep Order', default=False)
    wizard_create_id = fields.Integer('Wizard Create ID')
    post_id = fields.Many2one('sgeede.facebook.post', 'Post ID')


    def action_confirm(self):
        res = super(sale_order, self).action_confirm()
        invoice_lines = []
        for line in self.order_line:
            vals = {
                'name': line.name,
                'price_unit': line.price_unit,
                'quantity': line.product_uom_qty,
                'product_id': line.product_id.id,
                'product_uom_id': line.product_uom.id,
                'tax_ids': [(6, 0, line.tax_id.ids)],
                'sale_line_ids': [(6, 0, [line.id])],
            }
            invoice_lines.append((0, 0, vals))
        self.env['account.move'].create({
            'ref': self.client_order_ref,
            'move_type': 'out_invoice',
            'invoice_origin': self.name,
            'invoice_user_id': self.user_id.id,
            'partner_id': self.partner_invoice_id.id,
            'currency_id': self.company_id.currency_id.id,
            'invoice_line_ids': invoice_lines
        })
        return res

class sale_order_line(models.Model):
    _inherit = "sale.order.line"

    keep_id = fields.Many2one('my.future.keep.order', 'Keep ID')
    comment_id = fields.Many2one('sgeede.facebook.comment', 'Comment ID')
    size_id = fields.Many2one('my.future.product.size', 'Size')
    color = fields.Char("Warna", related="product_id.color")
    weight = fields.Float("Berat", related="product_id.weight")