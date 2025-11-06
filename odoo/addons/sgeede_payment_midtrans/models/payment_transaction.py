# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from werkzeug import urls

from odoo import _, api, models
from odoo.exceptions import ValidationError

from odoo.addons.payment_buckaroo.const import STATUS_CODES_MAPPING
from odoo.addons.payment_buckaroo.controllers.main import BuckarooController
import midtransclient
#pip install midtransclient


_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
	_inherit = 'payment.transaction'

	def _get_specific_rendering_values(self, processing_values):
		""" Override of payment to return Paypal-specific rendering values.

		Note: self.ensure_one() from `_get_processing_values`

		:param dict processing_values: The generic and specific processing values of the transaction
		:return: The dict of provider-specific processing values
		:rtype: dict
		"""
		res = super()._get_specific_rendering_values(processing_values)
		if self.provider_code not in ['midtrans', 'midtrans_sanskara', 'midtrans_sentosa', 'midtrans_abyakta']:
			return res

		base_url = self.provider_id.get_base_url()
		order_id = self.reference
		gross_amount = self.amount

		if self.provider_id.midtrans_setting()['midtrans_environment'] == 'test':
			snap = midtransclient.Snap(
				is_production=False,
				client_key=self.provider_id.midtrans_setting()['midtrans_client_key'],
				server_key=self.provider_id.midtrans_setting()['midtrans_server_key'])
		
		
		elif self.provider_id.midtrans_setting()['midtrans_environment'] == 'prod':
			# print ('sukses123123123123123123123213123',self.provider_id.midtrans_setting()['midtrans_client_key'])
			snap = midtransclient.Snap(
			is_production=True,
			client_key=self.provider_id.midtrans_setting()['midtrans_client_key'],
			server_key=self.provider_id.midtrans_setting()['midtrans_server_key']
			)
		# Prepare parameter

		# param = {
		# 	"transaction_details": {
		# 		"order_id": order_id,
		# 		"gross_amount": gross_amount
		# 	}, "credit_card":{
		# 		"secure" : True
		# 	}
		# }
		# prepare SNAP API parameter ( refer to: https://snap-docs.midtrans.com ) this is full parameter including optionals parameter.
		param = {
		    "transaction_details": {
		        "order_id": order_id,
		        "gross_amount": gross_amount
		    },
		    "item_details": [{
		        "id": "TOPUP_SALDO",
		        "price": gross_amount,
		        "quantity": 1,
		        "name": "TOP UP Saldo",
		        "brand": "SGEEDE",
		        "category": "SGEEDE",
		        "merchant_name": "SGEEDE"
		    }],
		    "customer_details": {
		        "first_name": self.partner_id.name,
		        "last_name": "",
		        "email": self.partner_id.email,
		        "phone": self.partner_id.phone,
		        "billing_address": {
		            "first_name": self.partner_id.name,
		            "last_name": "",
		            "email": self.partner_id.email,
		            "phone": self.partner_id.phone,
		            "address": self.partner_id.street,
		            "city": self.partner_id.city,
		            "postal_code": self.partner_id.zip,
		            "country_code": "IDN"
		        },
		        "shipping_address": {
		            "first_name": self.partner_id.name,
		            "last_name": "",
		            "email": self.partner_id.email,
		            "phone": self.partner_id.phone,
		            "address": self.partner_id.street,
		            "city": self.partner_id.city,
		            "postal_code": self.partner_id.zip,
		            "country_code": "IDN"
		        }
		    },
		    "enabled_payments": ["credit_card", "mandiri_clickpay", "cimb_clicks","bca_klikbca", "bca_klikpay", "bri_epay", "echannel", "indosat_dompetku","mandiri_ecash", "permata_va", "bca_va", "bni_va", "other_va", "gopay","kioson", "indomaret", "gci", "danamon_online"],
		    "credit_card": {
		        "secure": True,
		        "bank": "bca",
		        "installment": {
		            "required": False,
		            "terms": {
		                "bni": [3, 6, 12],
		                "mandiri": [3, 6, 12],
		                "cimb": [3],
		                "bca": [3, 6, 12],
		                "offline": [6, 12]
		            }
		        },
		        "whitelist_bins": [
		            "48111111",
		            "41111111"
		        ]
		    },		    
		   
		    "custom_field1": "custom field 1 content",
		    "custom_field2": "custom field 2 content",
		    "custom_field3": "custom field 3 content"
		}
		transaction = snap.create_transaction(param)

		transaction_redirect_url = transaction['redirect_url']

		return {
			'api_url': transaction_redirect_url,
		}

	def _get_tx_from_notification_data(self, provider_code, notification_data):
		""" Override of payment to find the transaction based on Paypal data.

		:param str provider_code: The code of the provider that handled the transaction
		:param dict notification_data: The notification data sent by the provider
		:return: The transaction if found
		:rtype: recordset of `payment.transaction`
		:raise: ValidationError if the data match no transaction
		"""
		tx = super()._get_tx_from_notification_data(provider_code, notification_data)
		if provider_code not in ['midtrans', 'midtrans_sanskara', 'midtrans_sentosa', 'midtrans_abyakta'] or len(tx) == 1:
			return tx


		reference = notification_data.get('order_id')
		tx = self.search([('reference', '=', reference), ('provider_code', 'ilike', 'midtrans')])
		if not tx:
			raise ValidationError(
				"Midtrans: " + _("No transaction found matching reference %s.", reference)
			)
		return tx

	def _process_notification_data(self, notification_data):
		""" Override of payment to process the transaction based on Paypal data.

		Note: self.ensure_one()

		:param dict notification_data: The notification data sent by the provider
		:return: None
		:raise: ValidationError if inconsistent data were received
		"""

		
		super()._process_notification_data(notification_data)
		if self.provider_code not in ['midtrans', 'midtrans_sanskara', 'midtrans_sentosa', 'midtrans_abyakta']:
			return

		#{'order_id': 'S00008-1', 'status_code': '200', 'transaction_status': 'settlement'}

		txn_id = notification_data.get('order_id')
		txn_type = notification_data.get('transaction_status')
		order_id  = notification_data.get('order_id')
		if not all((txn_id, txn_type)):
			raise ValidationError(
				"Midtrans: " + _(
					"Missing value for txn_id (%(txn_id)s) or txn_type (%(txn_type)s).",
					txn_id=txn_id, txn_type=txn_type
				)
			)
		self.provider_reference = txn_id
		# self.paypal_type = txn_type

		payment_status = notification_data.get('transaction_status')
		
		if payment_status == 'pending':
			self._set_pending(state_message="Pending")

		elif payment_status in ('settlement','success','capture'):
			#check again in midtranss
			#sss
			# Create Core API / Snap instance (both have shared `transactions` methods)
			print ("Check payment status")
			if self.provider_id.midtrans_setting()['midtrans_environment'] == 'test':
				api_client = midtransclient.CoreApi(
					is_production=False,
					client_key=self.provider_id.midtrans_setting()['midtrans_client_key'],
					server_key=self.provider_id.midtrans_setting()['midtrans_server_key']
				)

			if self.provider_id.midtrans_setting()['midtrans_environment'] == 'prod':
				api_client = midtransclient.CoreApi(
					is_production=True,
					client_key=self.provider_id.midtrans_setting()['midtrans_client_key'],
					server_key=self.provider_id.midtrans_setting()['midtrans_server_key']
				)

			mock_notification = {
				'currency': 'IDR',
				'fraud_status': 'accept',
				'gross_amount': self.amount,
				'order_id': order_id,
				'payment_type': 'bank_transfer',
				'status_code': '201',
				'status_message': 'Success, Bank Transfer transaction is created',
				'transaction_id': txn_id,
				'transaction_status': 'pending',
				#'transaction_time': '2018-10-24 15:34:33',
				#'va_numbers': [{'bank': 'bca', 'va_number': '490526303019299'}]
			}
			status_response = api_client.transactions.notification(mock_notification)

			order_id = status_response['order_id']
			transaction_status = status_response['transaction_status']
			fraud_status = status_response['fraud_status']
			print ('Transaction notification received. Order ID',order_id,'Transaction status:',transaction_status,'Fraud status:',fraud_status)
			# print('Transaction notification received. Order ID: {0}. Transaction status: {1}. Fraud status: {3}'.format(order_id,
			# 	transaction_status,
			# 	fraud_status))

			# Sample transaction_status handling logic
			
			if transaction_status == 'capture' or transaction_status == 'settlement':
				if fraud_status == 'challenge':
					# TODO set transaction status on your databaase to 'challenge'
					print ('challenge')
				elif fraud_status == 'accept':
					print ('test_set_done')
					self._set_done()
					# TODO set transaction status on your databaase to 'success'
			elif transaction_status == 'cancel' or	transaction_status == 'deny' or	transaction_status == 'expire':
				# TODO set transaction status on your databaase to 'failure'
				self._set_canceled()
			elif transaction_status == 'pending':
				# TODO set transaction status on your databaase to 'pending' / waiting payment
				print ('Pending')
				self._set_pending(state_message="Pending")
				#self._set_done()
		elif payment_status in ('cancel','deny','expire','refund','failure'):
			self._set_canceled()
		else:
			_logger.info(
				"received data with invalid payment status (%s) for transaction with reference %s",
				payment_status, self.reference
			)
			self._set_error(
				"Midtrans: " + _("Received data with invalid payment status: %s", payment_status)
			)


	   