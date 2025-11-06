# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from psycopg2 import sql

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'
    _description = 'Payment Provider'

    
    code = fields.Selection(
        selection_add=[('midtrans', "Midtrans")], ondelete={'midtrans': 'set default'})
    midtrans_test_id_merchant = fields.Char('Merchant ID (Sandbox)')
    midtrans_test_client_key = fields.Char('Client Key (Sandbox)')
    midtrans_test_server_key = fields.Char('Server Key (Sandbox)')
    midtrans_prod_id_merchant = fields.Char('Merchant ID')
    midtrans_prod_client_key = fields.Char('Client Key')
    midtrans_prod_server_key = fields.Char('Server Key')


    def midtrans_setting(self):
        values = {
            'midtrans_id_merchant' : self.midtrans_prod_id_merchant,
            'midtrans_client_key' : self.midtrans_prod_client_key,
            'midtrans_server_key' : self.midtrans_prod_server_key,
            'midtrans_environment': 'prod',
        }
        if self.state == 'test':
            values.update({
            'midtrans_id_merchant' : self.midtrans_test_id_merchant,
            'midtrans_client_key' : self.midtrans_test_client_key,
            'midtrans_server_key' : self.midtrans_test_server_key,
            'midtrans_environment': 'test',
            # G482287816
            # SB-Mid-client-vrI3y68MKynGkT35
            # SB-Mid-server-VK7_3AaNHk5l-pnUEZvuJyFY
        })
        return values


    def _midtrans_get_api_url(self):
        """ Return the API URL according to the provider state.

        Note: self.ensure_one()

        :return: The API URL
        :rtype: str
        """
        self.ensure_one()
        
        if self.state == 'enabled':
            return 'https://api.midtrans.com'
        else:
            return 'https://app.sandbox.midtrans.com/payment-links/for-payment-laundry-23-05-25-004'
            #return 'https://api.sandbox.midtrans.com'

    def midtrans_form_generate_values(self, values):
        values['client_key'] = self.midtrans_client_key
        if self.state == 'enabled':
            values['snap_js_url'] = 'https://app.midtrans.com/snap/snap.js'
        else:
            values['snap_js_url'] = 'https://app.sandbox.midtrans.com/snap/snap.js'
            

        if not 'return_url' in values:
            values['return_url'] = '/'

        values['order'] = request.website.sale_get_order()

        amount = values['amount']
        currency = values['currency']

        # You must have currency IDR enabled
        currency_IDR = self.env['res.currency'].search([('name', '=',
                'IDR')], limit=1)

        assert currency_IDR.name == 'IDR'

        # Convert to IDR
        if currency.id != currency_IDR.id:
            values['amount'] = int(round(currency.compute(amount,
                    currency_IDR)))

            values['currency'] = currency_IDR
            values['currency_id'] = currency_IDR.id
        else:
            values['amount'] = int(round(amount))

        return values


    def get_backend_endpoint(self):
        if self.state == 'enabled':
            return 'https://app.midtrans.com/snap/v1/transactions'
        return 'https://app.sandbox.midtrans.com/snap/v1/transactions'
        