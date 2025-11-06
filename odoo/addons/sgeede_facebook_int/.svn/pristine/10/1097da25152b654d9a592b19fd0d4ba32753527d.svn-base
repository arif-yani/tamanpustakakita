from odoo import api, fields, models
import time
from datetime import datetime, timedelta
import requests
import json
from odoo.exceptions import UserError, ValidationError

class sgeede_facebook_page(models.Model):
    _name = "sgeede.facebook.page"
    _description = "Facebook Page"


    name = fields.Char('Name')
    page_id = fields.Char('Page ID')
    user_account = fields.Char('User Account')
    page_token = fields.Char('Page Token')
    user_token = fields.Char('User Token')
    active = fields.Boolean(default=True)

    def cron_generate_token_data(self):
        api_url = "https://graph.facebook.com/v19.0/"
        page_obj = self.env["sgeede.facebook.page"].search([])
        for line in page_obj:
            api_get_pages_access_token = api_url+line.page_id+"?fields=access_token&access_token="+line.user_token
            headers = {
                'Content-Type':'application/json'
            }
            response_page = requests.get(api_get_pages_access_token, headers=headers)
            page_json = response_page.json()
            if 'access_token' not in page_json:
                self.env['sgeede.facebook.api.log'].create({
                    'name': 'Get Page Token',
                    'page_id': self.id,
                    'running_date': datetime.now(),
                    'state': 'failed',
                    'message': page_json,
                })
                return False
            line.page_token = page_json['access_token']
            self.env['sgeede.facebook.api.log'].create({
                'name': 'Get Page Token',
                'page_id': self.id,
                'running_date': datetime.now(),
                'state': 'success',
                'message': page_json,
            })
            return True