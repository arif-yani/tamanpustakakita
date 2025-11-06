import time

from odoo import SUPERUSER_ID 
from odoo import api, fields, models
from odoo import tools
import math
from odoo.tools import ustr
from odoo.http import request
from odoo.tools.translate import _
from odoo.exceptions import UserError

from odoo.addons.my_future_custom.controllers.rajaongkir import RajaOngkir

class Website(models.Model):
    _inherit = "website"

    def get_rajaongkir_city(self, partner_id):
        partner = request.env.user.partner_id
        partner_id = int(partner)
        results = RajaOngkir().get_all_city()
        rajaongkir_city = self.env['res.partner'].browse(partner_id).rajaongkir_city
        data = []
        for res in results:
            name = res['city_name'] + ', ' + res['province'] 
            data.append({ 'id':res['city_id'], 'name':name, 'selected': 1 if rajaongkir_city == res['city_id'] else 0 })
        return data

    def call_total_cashback(self): 
        context = self._context
        current_uid = context.get('uid') or self.env.user.id
        user = self.env['res.users'].browse(current_uid)
        partner = user.partner_id
        return partner.total_cashback

    def call_get_cashback(self, product_variant_id):
        cashback = self.env['olshop.range.cashback'].search([('product_id.id', '=', product_variant_id)])
        return cashback

    def get_user_aloy(self): 
        context = self._context
        current_uid = context.get('uid') or self.env.user.id
        return current_uid

    def get_current_pricelist(self):
        """
        :returns: The current pricelist record
        """
        self = self.with_company(self.company_id)
        ProductPricelist = self.env['product.pricelist']

        pricelist = ProductPricelist
        if request and request.session.get('website_sale_current_pl'):
            # `website_sale_current_pl` is set only if the user specifically chose it:
            #  - Either, he chose it from the pricelist selection
            #  - Either, he entered a coupon code
            pricelist = ProductPricelist.browse(request.session['website_sale_current_pl']).exists().sudo()
            country_code = self._get_geoip_country_code()
            if not pricelist or not pricelist._is_available_on_website(self) or not pricelist._is_available_in_country(country_code):
                request.session.pop('website_sale_current_pl')
                pricelist = ProductPricelist

        if not pricelist:
            partner_sudo = self.env.user.partner_id

            # If the user has a saved cart, it take the pricelist of this last unconfirmed cart
            pricelist = partner_sudo.last_website_so_id.pricelist_id
            if not pricelist:
                # The pricelist of the user set on its partner form.
                # If the user is not signed in, it's the public user pricelist
                pricelist = partner_sudo.property_product_pricelist

            # The list of available pricelists for this user.
            # If the user is signed in, and has a pricelist set different than the public user pricelist
            # then this pricelist will always be considered as available
            available_pricelists = self.get_pricelist_available()
            if available_pricelists and pricelist not in available_pricelists:
                # If there is at least one pricelist in the available pricelists
                # and the chosen pricelist is not within them
                # it then choose the first available pricelist.
                # This can only happen when the pricelist is the public user pricelist and this pricelist is not in the available pricelist for this localization
                # If the user is signed in, and has a special pricelist (different than the public user pricelist),
                # then this special pricelist is amongs these available pricelists, and therefore it won't fall in this case.
                pricelist = available_pricelists[0]

            if not pricelist:
                _logger.error(
                    'Failed to find pricelist for partner "%s" (id %s)',
                    partner_sudo.name, partner_sudo.id,
                )
        price_partner = self.env.user.partner_id
        if price_partner:
            if price_partner.property_product_pricelist:
                if pricelist.id != price_partner.property_product_pricelist.id:
                    pricelist = price_partner.property_product_pricelist
        return pricelist

    # Rajaongkir City Account
    def get_rajaongkir_city_account(self):
        data = []
        partner = request.env.user.partner_id
        rajaongkir_city = self.env['res.partner'].browse(int(partner)).rajaongkir_city
        results = RajaOngkir().get_all_city()

        for res in results:
            name = res['city_name'] + ', ' + res['province']
            data.append({ 'id':res['city_id'], 'name':name, 'selected': 1 if rajaongkir_city == res['city_id'] else 0 })

            if rajaongkir_city:
                if rajaongkir_city == res['city_id']:
                    partner.rajaongkir_city_name = res['city_name']
                    partner.rajaongkir_province_name = res['province']

        return data