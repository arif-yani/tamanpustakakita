# -*- encoding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class ResPartner(models.Model):
    _inherit = "res.partner"
	
    facebook_account_id = fields.Char('Facebook Account ID')

class sgeede_keep_order(models.Model):
    _name = "sgeede.keep.order"