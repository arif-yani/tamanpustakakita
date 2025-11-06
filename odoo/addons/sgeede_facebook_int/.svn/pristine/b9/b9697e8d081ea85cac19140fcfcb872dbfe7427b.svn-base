import json
import time
from datetime import datetime, timedelta
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from requests.models import PreparedRequest

req = PreparedRequest()

class sgeede_facebook_api_log(models.Model):
    _name = "sgeede.facebook.api.log"
    _description = "facebook API Logs"
    _order = "create_date desc"

    name = fields.Char('Name')
    page_id = fields.Many2one('sgeede.facebook.page', 'Page')
    running_date = fields.Datetime('Running Date')
    state = fields.Selection(selection=[('failed', 'Failed'), ('success', 'Success')], string='Status', store=True)
    message = fields.Html('Message')


# class sgeede_facebook_api_log_line(models.Model):
#     _name = "sgeede.facebook.api.log.line"