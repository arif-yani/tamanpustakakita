from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta

class my_future_summary_product_keep(models.TransientModel):
    _name = "my.future.summary.product.keep"

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    product_ids = fields.Many2many('product.product', 'summary_id', string='Product')


    def summary_product_keep(self):
        result = []
        keep_order_group_product = {
            product: count
            for product, count in self.env['my.future.keep.order']._read_group(
                domain=[('state', '=', 'order_supplier'), 
                        ('product_id','in',self.product_ids.ids)],
                groupby=['product_id'],
                aggregates=['__count'],
            )
        }
        print("check_masuk", keep_order_group_product)
        for product in keep_order_group_product.keys():
            keep_order_group_size = {
                size: count
                for size, count in self.env['my.future.keep.order']._read_group(
                    domain=[('product_id', '=', product.id), ('state', '=', 'order_supplier'),
                            ('product_id','in',self.product_ids.ids)],
                    groupby=['size_id'],
                    aggregates=['__count'],
                )
            }
            for size in keep_order_group_size.keys():
                vals = {}
                vals['product'] = product
                vals['size'] = size
                vals['pcs'] = self.get_total_pcs(product, size)
                result.append(vals)
        return result
    
    def get_total_pcs(self, product_id, size_id):
        domain=[('product_id', '=', product_id.id), ('state', '=', 'order_supplier'),
                 ('product_id','in',self.product_ids.ids), ('size_id', '=', size_id.id)]
        
        keep_obj = self.env['my.future.keep.order'].search(domain)
        pcs = 0
        for keep in keep_obj:
            pcs += keep.quantity
        return pcs
    
    def action_summary_product_keep(self):
        # self.summary_product_keep()
        return self.env.ref('my_future_custom.action_summary_product_keep_xls').report_action(self, config=False)