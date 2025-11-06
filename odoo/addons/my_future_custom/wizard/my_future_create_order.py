from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta

class my_future_create_order(models.TransientModel):
    _name = "my.future.create.order"

    def _get_default_product(self):
        product_ids = self.env['my.future.keep.order'].search([('state','=','order_supplier'),('get_product','=','dapat')]).product_id.ids
        return [('id','in',product_ids)]

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    product_ids = fields.Many2many('product.product', 'wizard_id', string='Product', domain=_get_default_product)

    def create_total_order(self):
        keep_order_group_customer = {
                customer
                for customer, count in self.env['my.future.keep.order']._read_group(
                    domain=[('state', '=', 'order_supplier'),('get_product', '=', 'dapat')],
                    groupby=['partner_id'],
                    aggregates=['__count'],
                )
            }
        if keep_order_group_customer:
            for partner_id in keep_order_group_customer:
                total_weight = 0
                keep_obj = self.env['my.future.keep.order'].search([('partner_id','=',partner_id.id), ('get_product', '=', 'dapat'),('state', '=', 'order_supplier'),('product_id', 'in', self.product_ids.ids)])
                invoice_obj = self.env['account.move'].create({
                    'partner_id': partner_id.id,
                    # 'is_keep_order': True,
                    'wizard_create_id': self.id,
                    'move_type': "out_invoice",
                    'date': datetime.today(),
                    'invoice_date': datetime.today(),
                    'invoice_payment_term_id': False,
                    'invoice_date_due': datetime.today() + timedelta(days=2)
                })
                # invoice_obj.harga_ongkir = invoice_obj.get_harga_ongkir(partner_id)
                if keep_obj:
                    for keep in keep_obj:
                        if keep.product_id in self.product_ids:
                            self.env['account.move.line'].create({
                                'product_id': keep.product_id.id,
                                'quantity': keep.quantity,
                                'move_id': invoice_obj.id,
                                'size_id': keep.size_id.id,
                                'keep_id': keep.id,
                                'comment_id': keep.comment_id.id,
                            })
                            total_weight += keep.product_id.weight
                            keep.state = 'totalan'
                        else:
                            invoice_obj.unlink()
                            continue
                    print("check_inv", invoice_obj)
                    self.env['account.move.line'].create({
                        'name': "Total Ongkir",
                        'price_unit': invoice_obj.get_harga_ongkir(partner_id),
                        'move_id': invoice_obj.id,
                        'quantity':  self.create_paket_line(invoice_obj),
                    })
                    invoice_obj.action_post()
                    count = 0
                    for paket in invoice_obj.paket_line_ids:
                        if not paket.parent_paket_id or not paket.name:
                            count += 1
                            paket.name = '%s-%s'%(invoice_obj.name or False, count)
                else:
                    invoice_obj.unlink()
            return {
                    'type': 'ir.actions.act_window',
                    'name': ('Invoices'),
                    'res_model': 'account.move',
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'domain': [('wizard_create_id','=',self.id)],
                    'context':{},
                }
        else:
            raise UserError('No keep order to create sale order!')
        
    def create_paket_line(self, invoice):
        myfuture_paket = self.env['myfuture.paket']
        total_weight = round(invoice.total_weight, 2)
        count = 0
        if invoice.partner_id.kota_id and invoice.partner_id.kota_id.name.upper() != "KOTA BATAM":
            while total_weight >= 1.3:
                count += 1
                myfuture_paket.create({
                    'weight': 1.3,
                    'move_id': invoice.id,
                    'ongkir_paket_state': 'lunas',
                })
                total_weight -= 1.3
            paket_obj = self.env['myfuture.paket'].search([('move_id','!=',invoice.id),('is_hide_paket','=',False),('partner_id','=',invoice.partner_id.id),('is_titipan','=',True)])
            for paket in paket_obj:
                if round(total_weight, 2) > 0.00 and paket.weight + round(total_weight, 2) <= 1.3:
                    count += 1
                    myfuture_paket.create({
                        'weight': paket.weight + round(total_weight, 2),
                        'move_id': invoice.id,
                        'ongkir_paket_state': 'lunas_prev_invoice' if  paket.ongkir_paket_state in ('lunas', 'lunas_prev_invoice') else 'lunas',
                        'parent_paket_id': paket.id,
                    })
                    total_weight = 0
                    if paket.ongkir_paket_state == 'belum_lunas':
                        paket.ongkir_paket_state = 'lunas'
                    paket.is_hide_paket = True
                else:
                    count += 1
                    print("paket_titipan", paket.name)
                    myfuture_paket.create({
                        'name': paket.name,
                        'weight': paket.weight,
                        'move_id': invoice.id,
                        'parent_paket_id': paket.id,
                        'ongkir_paket_state': 'lunas_prev_invoice' if paket.ongkir_paket_state in ('lunas', 'lunas_prev_invoice') else 'lunas',
                    })
                    if paket.ongkir_paket_state == 'belum_lunas':
                        paket.ongkir_paket_state = 'lunas'
                    paket.is_hide_paket = True
            
            if round(total_weight, 2) > 0.00:
                myfuture_paket.create({
                    'weight': round(total_weight, 2),
                    'move_id': invoice.id,
                    'ongkir_paket_state': 'lunas',
                })
                count += 1
        else:
            if total_weight > 0:
                count += 1
                myfuture_paket.create({
                    'name': '%s-%s'%(invoice.name or False, count),
                    'weight': total_weight + invoice.partner_id.total_titipan,
                    'move_id': invoice.id,
                    'ongkir_paket_state': 'lunas',

                })
        return count