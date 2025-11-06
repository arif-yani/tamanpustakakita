import json
import time
from datetime import datetime, timedelta
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from requests.models import PreparedRequest

class sgeede_facebook_api_log(models.Model):
    _name = "my.future.whatsapp.log"
    _description = "Whatsapp API Logs"
    _order = "create_date desc"

    name = fields.Char('Name')
    status_code = fields.Char('Status Code')
    dst_number = fields.Char('Destination Number')
    partner_id = fields.Many2one('res.partner', string="Partner")
    running_date = fields.Datetime('Running Date')
    state = fields.Selection(selection=[('failed', 'Failed'), ('success', 'Success')], string='Status', store=True)
    message = fields.Html('Message')

