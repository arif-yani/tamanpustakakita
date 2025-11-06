from odoo import api, fields, models
import time
from datetime import datetime, timedelta
import requests
import json
from odoo.exceptions import UserError, ValidationError
from odoo.addons.sgeede_facebook_int.models.sgeede_facebook_comment import sgeede_facebook_comment
import html2text
import re

class sgeede_facebook_comment(models.Model):
    _inherit = "sgeede.facebook.comment"


    is_keep_order = fields.Boolean('Comment Keep Order', default=False)
    code_product = fields.Char("Code", related="product_id.default_code")

    def _check_type_size(self, product_id):
        return all(size.isdigit() for size in self.get_all_size_product(product_id))

    def _try_get_value(self,comment):
        comment_name = comment.name.lower()
        if 'keep' in comment_name:
            comment.is_keep_order = True
            split_comment = comment_name.split()
            size = False
            qty = 1
            for name in split_comment:
                try:
                    if self._check_type_size(comment.product_id):
                        if name in self.get_all_size_product(comment.product_id) and len(self.get_all_size_product(comment.product_id)) >= 1:
                            size = name
                            continue
                    int_qty = int(name)
                    qty = int_qty
                except:
                    if name in self.get_all_size_product(comment.product_id) and len(self.get_all_size_product(comment.product_id)) >= 1:
                        size = name
            if size and len(self.get_all_size_product(comment.product_id)) >= 1 or len(self.get_all_size_product(comment.product_id)) == 0:
                self._create_keep_order(comment, qty, size)
            else:
                self.send_need_size(comment)

    def send_need_size(self, comment_id):
        if not comment_id.is_replied:
            api_url = "https://graph.facebook.com/v19.0/"
            if comment_id.post_id:
                comment_id.post_id.page_id.cron_generate_token_data()
                api_post_comment = api_url+comment_id.post_id.page_id.page_id+"/messages?access_token="+comment_id.post_id.page_id.page_token
            else:
                comment_id.live_id.page_id.cron_generate_token_data()
                api_post_comment = api_url+comment_id.live_id.page_id.page_id+"/messages?access_token="+comment_id.live_id.page_id.page_token
            messager_obj =  self.env['whatsapp.template'].search([('template_name','=','customer_komentar_ulang')], limit=1)
            send_message_obj = self.env['whatsapp.composer'].create({
                    'wa_template_id': messager_obj.id,
                    'phone':comment_id.partner_id.mobile,
                    'res_ids': comment_id.ids,
                    'res_model': 'sgeede.facebook.comment',
                })
            body = send_message_obj._get_html_preview_whatsapp(rec=comment_id)
            headers = {
                    'Content-Type': 'application/json', 
                }
            reply_message = {
                "recipient":{
                    "comment_id": comment_id.comment_id.split("_")[1]
                },
                "messaging_type": "RESPONSE",
                "message":{
                    "text": html2text.html2text(body)
                }
            }
            response = requests.post(api_post_comment, headers=headers, data=json.dumps(reply_message))
            if response.status_code == 200:
                comment_id.is_replied = True

    def send_need_mobile(self, comment_id, keep_id):
        if not comment_id.is_replied:
            api_url = "https://graph.facebook.com/v19.0/"
            if comment_id.post_id:
                comment_id.post_id.page_id.cron_generate_token_data()
                api_post_comment = api_url+comment_id.post_id.page_id.page_id+"/messages?access_token="+comment_id.post_id.page_id.page_token
            else:
                comment_id.live_id.page_id.cron_generate_token_data()
                api_post_comment = api_url+comment_id.live_id.page_id.page_id+"/messages?access_token="+comment_id.live_id.page_id.page_token
            keep_order_obj = self.env['my.future.keep.order'].search([('partner_id','=',keep_id.partner_id.id),('state','=','waiting_wa')])
            body = False
            if keep_order_obj and len(keep_order_obj) >= 2:
                if len(keep_order_obj) >= 3:
                    keep_id.unlink()
                messager_obj =  self.env['whatsapp.template'].search([('template_name','=','waiting_wa_keep_reminder')], limit=1)
                send_message_obj = self.env['whatsapp.composer'].create({
                    'wa_template_id': messager_obj.id,
                    'phone':comment_id.partner_id.mobile,
                    'res_ids': comment_id.ids,
                    'res_model': 'sgeede.facebook.comment',
                })
                body = send_message_obj._get_html_preview_whatsapp(rec=comment_id)
            else:
                messager_obj =  self.env['whatsapp.template'].search([('template_name','=','messanger_request_number_phone')], limit=1)
                send_message_obj = self.env['whatsapp.composer'].create({
                        'wa_template_id': messager_obj.id,
                        'phone':keep_id.partner_id.mobile,
                        'res_ids': keep_id.ids,
                        'res_model': 'my.future.keep.order',
                    })
                body = send_message_obj._get_html_preview_whatsapp(rec=keep_id)
            message = html2text.html2text(body)
            message = message.replace("&gt;", "")
            message = message.replace("&lt;", "")
            headers = {
                    'Content-Type': 'application/json', 
                }
            reply_message = {
                "recipient":{
                    "comment_id": comment_id.comment_id.split("_")[1]
                },
                "messaging_type": "RESPONSE",
                "message":{
                    "text": message
                }
            }
            response = requests.post(api_post_comment, headers=headers, data=json.dumps(reply_message))
            if response.status_code == 200:
                comment_id.is_replied = True

    def get_all_size_product(self, product_id):
        return [size.name.lower().strip() for size in product_id.size_ids]

    def _create_keep_order(self, comment_id, pce, size):
        comment_obj = self.env['my.future.keep.order'].search([('comment_id','=',comment_id.id)])
        if not comment_id.partner_id.is_blacklist_customer:
            if comment_id.is_keep_order and not comment_obj:
                size_obj = False
                if size:
                    size_data = self.env['my.future.product.size'].search([('name','ilike',size)], limit=1)
                    if size_data in comment_id.product_id.size_ids:
                        size_obj = size_data
                order_obj = self.env['my.future.keep.order'].create({
                    'partner_id': comment_id.partner_id.id,
                    'keep_datetime': comment_id.created_comment_time,
                    'product_id': comment_id.product_id.id if comment_id.product_id else False,
                    'comment_id': comment_id.id,
                    'quantity': pce,
                    'state': 'keep' if comment_id.partner_id.mobile else 'waiting_wa',
                    'size_id': size_obj.id if size_obj else False,
                    })
                if order_obj and not comment_id.partner_id.mobile or order_obj.state == 'waiting_wa':
                    print("check_parter", order_obj.partner_id)
                    self.send_need_mobile(comment_id, order_obj)
                elif order_obj and order_obj.state == 'keep':
                    self.send_customer_message(comment_id, order_obj)
            elif comment_obj:
                size_obj = False
                size_data = self.env['my.future.product.size'].search([('name','ilike',size)], limit=1)
                if size_data in comment_id.product_id.size_ids:
                    size_obj = size_data
                comment_obj.write({
                    'partner_id': comment_id.partner_id.id,
                    'keep_datetime': comment_id.created_comment_time,
                    'product_id': comment_id.product_id.id if comment_id.product_id else False,
                    'comment_id': comment_id.id,
                    'state': 'keep' if comment_id.partner_id.mobile else 'waiting_wa',
                    'quantity': pce,
                    'size_id': size_obj.id if size_obj else False,
                    })
                if comment_obj and not comment_id.partner_id.mobile or comment_obj.state == 'waiting_wa':
                    self.send_need_mobile(comment_id, comment_obj)
                elif comment_obj and comment_obj.state == 'keep':
                    self.send_customer_message(comment_id, comment_obj)
        elif comment_id.partner_id.is_blacklist_customer and not comment_id.partner_id.is_announced:
            template_id =  self.env['whatsapp.template'].search([('template_name','=','blacklist_customer_message')], limit=1)
            send_message_obj = self.env['whatsapp.composer'].create({
                        'wa_template_id': template_id.id,
                        'phone':comment_id.partner_id.mobile,
                        'res_ids': comment_id.partner_id.ids,
                        'res_model': 'res.partner',
                    })
            send_message_obj.action_send_message_my_future()
            comment_id.partner_id.is_announced = True
     

    def create_comment(self, post_id, page_id):
        comments = self.get_all_comments(post_id, page_id)
        if comments:
            for comment in comments:
                get_same_comment = self.search([('comment_id','=', comment['id']),('post_id','=',post_id.id)])
                sender_comment = False
                sender_comment_id = False
                timestamp_str = comment['created_time']
                formatted_timestamp = timestamp_str.replace("T", " ")
                formatted_timestamp = formatted_timestamp.replace("+0000", "")
                datetime_obj = datetime.strptime(formatted_timestamp, "%Y-%m-%d %H:%M:%S")
                comment_user = None
                if 'from' in comment:
                    sender_comment = comment['from']['name']
                    sender_comment_id = comment['from']['id']
                    comment_user = self.env['res.partner'].search([('facebook_account_id','=',sender_comment_id)])
                    if not comment_user:
                        comment_user = self.env['res.partner'].create({
                            'name': sender_comment,
                            'facebook_account_id': sender_comment_id,
                            'customer_rank': 1,
                            'supplier_rank': 0,
                        })
                if not get_same_comment:
                    comment_obj = self.create({
                        'partner_id': comment_user.id if comment_user != None else False,
                        'name': comment['message'],
                        'comment_id': comment['id'],
                        'sender': sender_comment,
                        'sender_comment_id': sender_comment_id,
                        'created_comment_time': datetime_obj,
                        'post_id': post_id.id,
                        'id_attachment': comment['id_attachment'] if 'id_attachment' in comment else False,
                    })
                    if comment_obj.id_attachment:
                        post_attachment = self.env['sgeede.facebook.attachment'].search([('id_attachment','=',comment_obj.id_attachment)], limit=1)
                        comment_obj.product_id = post_attachment.product_id.id
                    self._try_get_value(comment_obj)
                else:
                    get_same_comment.update({
                        'partner_id': comment_user.id if comment_user != None else False,
                        'name': comment['message'],
                        'comment_id': comment['id'],
                        'sender': sender_comment,
                        'sender_comment_id': sender_comment_id,
                        'created_comment_time': datetime_obj,
                        'post_id': post_id.id,
                        'id_attachment': comment['id_attachment'] if 'id_attachment' in comment else '',

                    })
                    if get_same_comment.id_attachment:
                        post_attachment = self.env['sgeede.facebook.attachment'].search([('id_attachment','=',get_same_comment.id_attachment)], limit=1)
                        get_same_comment.product_id = post_attachment.product_id.id
                    self._try_get_value(get_same_comment)
    sgeede_facebook_comment.create_comment = create_comment

        
    def send_customer_message(self, comment_id, keep_id):
        if not comment_id.is_replied:
            api_url = "https://graph.facebook.com/v19.0/"
            api_post_comment = ''
            if comment_id.post_id:
                comment_id.post_id.page_id.cron_generate_token_data()
                api_post_comment = api_url+comment_id.post_id.page_id.page_id+"/messages?access_token="+comment_id.post_id.page_id.page_token
            else:
                comment_id.live_id.page_id.cron_generate_token_data()
                api_post_comment = api_url+comment_id.live_id.page_id.page_id+"/messages?access_token="+comment_id.live_id.page_id.page_token
            messager_obj =  self.env['whatsapp.template'].search([('template_name','=','messanger_confirm_keep_order')], limit=1)
            send_message_obj = self.env['whatsapp.composer'].create({
                    'wa_template_id': messager_obj.id,
                    'phone':keep_id.partner_id.mobile,
                    'res_ids': keep_id.ids,
                    'res_model': 'my.future.keep.order',
                })
            body = send_message_obj._get_html_preview_whatsapp(rec=keep_id)
            message = html2text.html2text(body)
            headers = {
                    'Content-Type': 'application/json', 
                }
            reply_message = {
                "recipient":{
                    "comment_id": comment_id.comment_id.split("_")[1]
                },
                "messaging_type": "RESPONSE",
                "message":{
                    "text": message
                }
            }
            response = requests.post(api_post_comment, headers=headers, data=json.dumps(reply_message))
            if response.status_code == 200:
                comment_id.is_replied = True
        

class sgeede_facebook_live(models.Model):
    _inherit = "sgeede.facebook.live"

    active_product = fields.Many2one('product.product', "Active Product")

    def create_comment(self):
        comments = self.get_all_comments()
        for comment in comments:
            sender_comment = False
            sender_comment_id = False
            if self.sum_comment > 0:
                if comment['id'] in [comment.comment_id for comment in self.comment_ids]:
                    continue
            timestamp_str = comment['created_time']
            formatted_timestamp = timestamp_str.replace("T", " ")
            formatted_timestamp = formatted_timestamp.replace("+0000", "")
            datetime_obj = datetime.strptime(formatted_timestamp, "%Y-%m-%d %H:%M:%S")
            comment_user = None
            if 'from' in comment:
                sender_comment = comment['from']['name']
                sender_comment_id = comment['from']['id']
                comment_user = self.env['res.partner'].search([('facebook_account_id','=',sender_comment_id)])
                if not comment_user:
                    comment_user = self.env['res.partner'].create({
                            'name': sender_comment,
                            'facebook_account_id': sender_comment_id,
                            'customer_rank': 1,
                            'supplier_rank': 0,
                        })
            comment_live = self.comment_ids.create({
                'partner_id': comment_user.id if comment_user != None else False,
                'name': comment['message'],
                'comment_id': comment['id'],
                'sender': sender_comment,
                'sender_comment_id': sender_comment_id,
                'created_comment_time': datetime_obj,
                'live_id': self.id,
            })
            self._try_get_product(comment_live)
            if self._check_valid_time_comment(comment_user, comment_live.live_id, comment_live):
                if comment_live.product_id:
                    comment_live._try_get_value(comment_live)

    def _check_valid_time_comment(self, partner_id, live_id, comment_now):
        get_previous_comment = self.env['sgeede.facebook.comment'].search([('partner_id','=',partner_id.id),('live_id','=',live_id.id),('is_keep_order','=',True)])
        vals = True
        for comment in get_previous_comment:
            if comment != comment_now:
                if comment_now.created_comment_time >= comment.created_comment_time + timedelta(minutes=1):
                    vals = True
                else:
                    return False
        return vals


    def _try_get_product(self,comment_live):
        comment_name = comment_live.name.lower()
        if 'keep' in comment_name:
            split_comment = comment_name.split()
            for name in split_comment:
                if comment_live.product_id:
                    break
                try:    
                    for active_product in self.line_ids:
                        if active_product.code_product.lower() == name:
                            comment_live.product_id = active_product.product_id.id
                            break
                except:
                    print("Cannot found product")
            if not comment_live.product_id:
                for active_product in self.line_ids:
                    if active_product.is_active_product:
                        comment_live.product_id = active_product.product_id.id

class sgeede_facebook_product(models.Model):
    _inherit = "sgeede.facebook.product"

    is_active_product = fields.Boolean("Active Product")
    size_ids = fields.Many2many('my.future.product.size', 'product_id', string='Size', related="product_id.size_ids")
    code_product = fields.Char("Code", related="product_id.default_code")

