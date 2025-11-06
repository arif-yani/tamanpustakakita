# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint

import requests
from werkzeug import urls
from werkzeug.exceptions import Forbidden

from odoo import _, http
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo.tools import html_escape

# http://operasabun.test:8069/sgeede_payment/midtrans/finish?order_id=S00008-1&status_code=200&transaction_status=settlement

_logger = logging.getLogger(__name__)
logger = logging.getLogger(__name__)

def _prune_dict(data):
	if isinstance(data, dict):
		return {key: _prune_dict(value)\
				for key, value in data.items() if value is not None}

	return data

class MidtransController(http.Controller):
	_return_url = '/sgeede_payment/midtrans/finish'
	_webhook_url = '/payment/midtrans/webhook/'

	
	def prepare_send_email(self, res):
		try: ##IMPORTANT check email on Paypal and Member to!
			mail_id = res.create_mail()
			try: 
				mail_id.send()
			except:
				_logger.warning("An Error occurred send Email!")
		except:
			_logger.warning("An Error occurred when create_mail")


	def check_transaction_status(self, transaction_id): 
		domain = [('midtrans_txn_id','=',transaction_id)]
		
		return_url = '/batambooking'


		return werkzeug.utils.redirect(return_url)

	def data_process(self, order_id, status, txn_id='', payment_type='',post={}):
		order_data = order_id.split('BID')
		booking_no = len(order_data) > 1 and order_data[1] or False
		domain = [('booking_no','=',booking_no),('is_payment_complete','=',False)]
		res = request.env['calendar.event'].sudo().search(domain, limit=1)
		action_type = post.get('action_type')
		is_json = post.get('is_json')

		if res:
			acquirer_id = res.payment_acquirer_id
			if acquirer_id.website_payment_type == 'midtrans':
				values = { 'midtrans_status' : str(status) }
				if txn_id:
					values['midtrans_txn_id'] = txn_id

				res.write(values)
				is_success = False
				is_pending = False

				booking_values = {
						'name' : '(Website - %s - %s)' % (str(res.partner_id.name), str(order_id))
					}
 
				if status in ['settlement','success','capture']:
					is_success = True
					booking_values['midtrans_status'] = 'success'

				if status in ['pending']: #Waiting payment
					is_success = False
					is_pending = True
					booking_values['midtrans_status'] = 'pending'

				if status in ['cancel','deny','expire','refund','failure']:
					is_success = False
					is_pending = False


				if is_success:
					res.write(booking_values)
					res.mark_complete_payment() 
					res.button_validate_transfer()
					self.prepare_send_email(res)

				if is_json:
					return {'success':True}

				if is_success or is_pending:
					self.reset_booking_session(res)
					return_url = '/batambooking/confirmation'
					if action_type == 'post':
						return 'ok'
					return werkzeug.utils.redirect(return_url)

		if is_json:
			return {'success':False}

		return werkzeug.utils.redirect('/batambooking')

	@http.route('/payment_booking/midtrans/notification', type='json', auth="public", methods=['POST'], csrf=False)
	def payment_booking_midtrans_notification(self, *args, **kwargs):
		data = request.jsonrequest 
		_logger.info('MIDTRANS SEND NOTIFICATION')
		_logger.info(data)   

		if data:
			order_id = data.get('order_id')
			status = data.get('transaction_status')
			txn_id = data.get('transaction_id')
			payment_type = data.get('payment_type')

			if order_id and status:
				data['is_json'] = True
				return self.data_process(order_id,status,txn_id,payment_type,post=data)

		return {'status': True}

	@http.route(_return_url, type='http', auth="none", methods=['POST', 'GET'], csrf=False)
	def payment_booking_midtrans_finish(self, **post):
		##?order_id=T-1580721033&status_code=201&transaction_status=pending
		
		_logger.info('MIDTRANS FINISH')
		_logger.info(post)

		order_id = post.get('order_id')
		status = post.get('transaction_status')
		txn_id = post.get('transaction_id')
		payment_type = post.get('payment_type')

		
		_logger.info("handling redirection from Midtrans with data:\n%s", pprint.pformat(post))
		if not post:  # The customer has canceled or paid then clicked on "Return to Merchant"
			pass  # Redirect them to the status page to browse the (currently) draft transaction
		else:
			# Check the origin of the notification
			tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_notification_data(
				'midtrans', post
			)		
			
			tx_sudo._handle_notification_data('midtrans', post)
		return request.redirect('/payment/status')
	

	@http.route(_webhook_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False)
	def midtrans_webhook(self, **data):
		""" Process the notification data (IPN) sent by PayPal to the webhook.

		The "Instant Payment Notification" is a classical webhook notification.
		See https://developer.midtrans.com/api/nvp-soap/ipn/.

		:param dict data: The notification data
		:return: An empty string to acknowledge the notification
		:rtype: str
		"""
		_logger.info("notification weebhook received from Midtrans with data:\n%s", pprint.pformat(data))
		try:
			# Check the origin and integrity of the notification
			tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_notification_data(
				'midtrans', data
			)
			# self._verify_webhook_notification_origin(data, tx_sudo)

			# Handle the notification data
			tx_sudo._handle_notification_data('midtrans', data)
		except ValidationError:  # Acknowledge the notification to avoid getting spammed
			_logger.exception("unable to handle the notification data; skipping to acknowledge")
		return ''
	
	@http.route('/payment/midtrans/unfinish', type='http', auth="none", methods=['POST', 'GET'], csrf=False)
	def payment_booking_midtrans_unfinish(self, **post):
		_logger.info('MIDTRANS UNFINISH')
		_logger.info(post)

		order_id = post.get('order_id')
		status = post.get('transaction_status')
		txn_id = post.get('transaction_id')
		payment_type = post.get('payment_type')
		# if order_id and status:
		# 	return self.data_process(order_id,status,txn_id,payment_type,post=post)
		_logger.info("handling redirection from Midtrans with data:\n%s", pprint.pformat(post))
		if not post:  # The customer has canceled or paid then clicked on "Return to Merchant"
			pass  # Redirect them to the status page to browse the (currently) draft transaction
		else:
			# Check the origin of the notification
			tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_notification_data(
				'midtrans', post
			)		
			
			tx_sudo._handle_notification_data('midtrans', post)
		return request.redirect('/payment/status')

	@http.route('/payment_booking/midtrans/error', type='http', auth="none", methods=['POST', 'GET'], csrf=False)
	def payment_booking_midtrans_error(self, **post):
		_logger.info('MIDTRANS ERROR')
		_logger.info(post)

		order_id = post.get('order_id')
		status = post.get('transaction_status')
		txn_id = post.get('transaction_id')
		payment_type = post.get('payment_type')
		if order_id and status:
			return self.data_process(order_id,status,txn_id,payment_type,post=post)
		return werkzeug.utils.redirect('/batambooking')


	@http.route('/midtrans/get_token', auth='user', type='json')
	def get_token(self, **post):
		acquirer_id = post.get('acquirer_id')
		if not acquirer_id:
			raise ValidationError('acquirer_id is required.')

		try:
			acquirer_id = int(acquirer_id)
		except (ValueError, TypeError):
			raise ValidationError('Invalid acquirer_id.')

		order_id = post.get('order_id')
		if not order_id:
			raise ValidationError('order_id is required.')

		try:
			order_id = int(order_id)
		except (ValueError, TypeError):
			raise ValidationError('Invalid order_id.')

		amount = post.get('amount')
		if not amount:
			raise ValidationError('amount is required.')

		try:
			amount = int(amount)
		except (ValueError, TypeError):
			raise ValidationError('Invalid amount.')

		reference = post.get('reference')
		if not reference:
			raise ValidationError('reference is required.')

		return_url = post.get('return_url')
		if not return_url:
			raise ValidationError('return_url is required.')

		acquirer = request.env['payment.provider'].sudo().browse(acquirer_id)
		order = request.env['sale.order'].sudo().browse(order_id)

		response = {
			'return_url': return_url,
		}

		headers = {
			'accept': 'application/json',
		}
		payload = {
			'transaction_details': {
				'order_id': reference,
				'gross_amount': amount,
			},
			'customer_details': {
				'first_name': post.get('partner_first_name'),
				'last_name': post.get('partner_last_name'),
				'email': post.get('partner_email'),
				'phone': post.get('partner_phone'),

				'billing_address': {
					'first_name': post.get('billing_partner_first_name'),
					'last_name': post.get('billing_partner_last_name'),
					'email': post.get('billing_partner_email'),
					'phone': post.get('billing_partner_phone'),
					'address': post.get('billing_partner_address'),
					'country_code': post.get('billing_partner_country_code'),
					'postal_code': post.get('billing_partner_postal_code'),
					'city': post.get('billing_partner_city'),
				},
			},
		}
		payload = _prune_dict(payload)
		resp = requests.post(acquirer.get_backend_endpoint(), json=payload,
				headers=headers, auth=(acquirer.midtrans_server_key, ''))

		if resp.status_code >= 200 and resp.status_code < 300:
			reply = resp.json()
			response['snap_token'] = reply['token']

		elif resp.text:
			reply = resp.json()
			if 'error_messages' in reply:
				response['snap_errors'] = resp.json().get('error_messages', [])

			else:
				_logger.warn('Unexpected Midtrans response: %i: %s',
						resp.status_code, resp.text)
		else:
			response['snap_errors'] = ['Unknown error.']

		return response

#===========
	@http.route('/midtrans/validate', auth='user', type='json')
	def payment_validate(self, **post):
		logger.error(repr(post))
		reference = post.get('reference')
		if not reference:
			raise ValidationError('reference is required.')

		status = post.get('transaction_status')
		if not status:
			raise ValidationError('transaction_status is required.')

		message = post.get('message')
		if not message:
			raise ValidationError('message is required.')

		tx = request.env['payment.transaction'].sudo().search([
				('reference', '=', reference)], limit=1)

		if (status == 'pending' and tx.state == 'draft') or\
				(status == 'done' and tx.state != 'done') or\
				status == 'error':

			tx.write({'state': status, 'state_message': message})

		order = tx.sale_order_id

		if status == 'done' and order.state != 'done':
			order.write({'state': 'done'})
		elif status == 'pending' and order.state not in ('done', 'sale'):
			order.write({'state': 'sale'})


	@http.route('/midtrans/notification', auth='none', csrf=False, type='json')
	def midtrans_notification(self, **post):
		logger.error(repr(post))

		reference = post.get('order_id')
		if not reference:
			raise ValidationError('order_id is required.')

		code = post.get('status_code')
		if not code:
			raise ValidationError('status_code is required.')

		tx_status = post.get('transaction_status')
		if not tx_status:
			raise ValidationError('transaction_status is required.')

		if code == '200':
			if tx_status in ('settlement', 'refund', 'chargeback',
					'partial_refund', 'partial_chargeback'):

				status = 'done'

			elif tx_status in ('cancel',):
				status = 'cancel'

			else:
				status = 'pending'
		elif code == '201':
			status = 'pending'
		else:
			status = 'error'

		message = post.get('status_message')
		if not message:
			raise ValidationError('status_message is required.')

		tx = request.env['payment.transaction'].sudo().search([
				('reference', '=', reference)], limit=1)

		## Security check

		acquirer = tx.acquirer_id
		signature_data = post['order_id'] + post['status_code'] +\
				post['gross_amount'] + acquirer.midtrans_server_key

		assert post['signature_key'] == sha512(signature_data).hexdigest()

		## Update database

		if (status == 'pending' and tx.state in ('draft', 'pending')) or\
				status in ('done', 'error', 'cancel'):

			tx.write({'state': status, 'state_message': message})

		order = tx.sale_order_id

		if status == 'done':
			order.write({'state': 'done'})
		elif status == 'pending' and order.state not in ('done',):
			order.write({'state': 'sale'})
		elif status in ('cancel', 'error'):
			order.write({'state': 'draft'})

		return {}