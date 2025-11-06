from odoo import api, fields, models
import time
from datetime import datetime, timedelta
import requests
import json
from odoo.exceptions import UserError, ValidationError

class myfuture_ongkir(models.Model):
    _name = "myfuture.ongkir"
    _description = "My Future Ongkir"

    name = fields.Char("Name", compute="_compute_name", store=True)
    price = fields.Monetary(string="Harga Ongkir", required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,default=lambda self: self.env.user.company_id.currency_id)
    provinsi_id = fields.Many2one("myfuture.provinsi", "Provinsi", related="kota_id.provinsi_id", readonly=False, store=True)
    kota_id = fields.Many2one("myfuture.kota", "Kabupaten/Kota", related="kecamatan_id.kota_id", readonly=False, store=True)
    kecamatan_id = fields.Many2one("myfuture.kecamatan", "Location", require=True)


    @api.depends('price')
    def _compute_display_name(self):
        for line in self:
            line.display_name = '%s'%(line.price or False)

    @api.depends('kecamatan_id', 'price')
    def _compute_name(self):
        for line in self:
            line.name = '%s-%s'%(line.kecamatan_id.name or False, line.price)