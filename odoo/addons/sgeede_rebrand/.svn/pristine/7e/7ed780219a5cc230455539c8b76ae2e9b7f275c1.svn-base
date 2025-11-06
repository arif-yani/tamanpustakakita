# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import logging
import os
from tempfile import TemporaryFile

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SgeedeEnterprise(models.TransientModel):
	_name = "sgeede.enterprise.text"
	_description = 'Sgeede Enterprise'

	name = fields.Char('Rebrand Name', required=True, default="SGEEDE ERP")


	def init(self):
		self._cr.execute(f"""UPDATE ir_actions SET help = REPLACE(help::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_actions SET help = REPLACE(help::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_ui_view SET arch_db = REPLACE(arch_db::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_ui_view SET arch_db = REPLACE(arch_db::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_ui_view SET arch_prev = REPLACE(arch_prev::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))""")
		self._cr.execute(f"""UPDATE ir_ui_view SET arch_prev = REPLACE(arch_prev::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))""")
		self._cr.execute(f"""UPDATE ir_ui_view_custom SET arch = REPLACE(arch::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_ui_view_custom SET arch = REPLACE(arch::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE mail_template SET body_html = REPLACE(body_html::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE mail_template SET body_html = REPLACE(body_html::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE mail_template SET subject = REPLACE(subject::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE mail_template SET subject = REPLACE(subject::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE mail_template SET name = REPLACE(name::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE mail_template SET name = REPLACE(name::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE res_partner SET name = REPLACE(name::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))""")
		self._cr.execute(f"""UPDATE res_partner SET name = REPLACE(name::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))""")
		self._cr.execute(f"""UPDATE res_partner SET email = REPLACE(email::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))""")
		self._cr.execute(f"""UPDATE res_partner SET email = REPLACE(email::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))""")
		self._cr.execute(f"""UPDATE res_partner SET website = REPLACE(website::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))""")
		self._cr.execute(f"""UPDATE res_partner SET website = REPLACE(website::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))""")
		self._cr.execute(f"""UPDATE ir_model_fields SET help = REPLACE(help::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_model_fields SET help = REPLACE(help::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_model_fields SET field_description = REPLACE(field_description::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_model_fields SET field_description = REPLACE(field_description::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_model_fields_selection SET name = REPLACE(name::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))::jsonb""")		
		self._cr.execute(f"""UPDATE ir_model_fields_selection SET name = REPLACE(name::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))::jsonb""")		
		self._cr.execute(f"""UPDATE ir_actions SET help = REPLACE(help::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_ui_view SET arch_db = REPLACE(arch_db::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_ui_view SET arch_db = REPLACE(arch_db::text, (CAST ('Odoo S.A.' AS text)), (CAST ('SGEEDE ERP' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_ui_view SET arch_db = REPLACE(arch_db::text, (CAST ('odoo.com' AS text)), (CAST ('sgeede.com' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_ui_view SET arch_prev = REPLACE(arch_prev::text, (CAST ('odoo.com' AS text)), (CAST ('sgeede.com' AS text)))""")
		self._cr.execute(f"""UPDATE ir_ui_view SET arch_prev = REPLACE(arch_prev::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))""")
		self._cr.execute(f"""UPDATE ir_ui_view_custom SET arch = REPLACE(arch::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_ui_view_custom SET arch = REPLACE(arch::text, (CAST ('odoo.com' AS text)), (CAST ('sgeede.com' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE mail_template SET body_html = REPLACE(body_html::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE mail_template SET body_html = REPLACE(body_html::text, (CAST ('odoo.com' AS text)), (CAST ('sgeede.com' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE mail_template SET subject = REPLACE(subject::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE mail_template SET name = REPLACE(name::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE mail_template SET email_from = REPLACE(email_from::text, (CAST ('odoo.com' AS text)), (CAST ('sgeede.com' AS text)))""")
		self._cr.execute(f"""UPDATE res_partner SET name = REPLACE(name::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))""")
		self._cr.execute(f"""UPDATE res_partner SET email = REPLACE(email::text, (CAST ('odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))""")
		self._cr.execute(f"""UPDATE res_partner SET website = REPLACE(website::text, (CAST ('odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))""")
		self._cr.execute(f"""UPDATE ir_model_fields SET help = REPLACE(help::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_model_fields SET field_description = REPLACE(field_description::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_model_fields_selection SET name = REPLACE(name::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))::jsonb""")		
		self._cr.execute(f"""UPDATE ir_ui_view SET name = REPLACE(name::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))""")

	def enterprise_text(self):
		self._cr.execute(f"""UPDATE ir_actions SET help = REPLACE(help::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_actions SET help = REPLACE(help::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_ui_view SET arch_db = REPLACE(arch_db::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_ui_view SET arch_db = REPLACE(arch_db::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_ui_view SET arch_prev = REPLACE(arch_prev::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))""")
		self._cr.execute(f"""UPDATE ir_ui_view SET arch_prev = REPLACE(arch_prev::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))""")
		self._cr.execute(f"""UPDATE ir_ui_view_custom SET arch = REPLACE(arch::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_ui_view_custom SET arch = REPLACE(arch::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE mail_template SET body_html = REPLACE(body_html::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE mail_template SET body_html = REPLACE(body_html::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE mail_template SET subject = REPLACE(subject::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE mail_template SET subject = REPLACE(subject::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE mail_template SET name = REPLACE(name::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE mail_template SET name = REPLACE(name::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE res_partner SET name = REPLACE(name::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))""")
		self._cr.execute(f"""UPDATE res_partner SET name = REPLACE(name::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))""")
		self._cr.execute(f"""UPDATE res_partner SET email = REPLACE(email::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))""")
		self._cr.execute(f"""UPDATE res_partner SET email = REPLACE(email::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))""")
		self._cr.execute(f"""UPDATE res_partner SET website = REPLACE(website::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))""")
		self._cr.execute(f"""UPDATE res_partner SET website = REPLACE(website::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))""")
		self._cr.execute(f"""UPDATE ir_model_fields SET help = REPLACE(help::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_model_fields SET help = REPLACE(help::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_model_fields SET field_description = REPLACE(field_description::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_model_fields SET field_description = REPLACE(field_description::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_model_fields_selection SET name = REPLACE(name::text, (CAST ('Odoobot' AS text)), (CAST ('SGEEDEbot' AS text)))::jsonb""")		
		self._cr.execute(f"""UPDATE ir_model_fields_selection SET name = REPLACE(name::text, (CAST ('OdooBot' AS text)), (CAST ('SGEEDEBot' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_actions SET help = REPLACE(help::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_ui_view SET arch_db = REPLACE(arch_db::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_ui_view SET arch_db = REPLACE(arch_db::text, (CAST ('Odoo S.A.' AS text)), (CAST ('SGEEDE ERP' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_ui_view SET arch_db = REPLACE(arch_db::text, (CAST ('odoo.com' AS text)), (CAST ('sgeede.com' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_ui_view SET arch_prev = REPLACE(arch_prev::text, (CAST ('odoo.com' AS text)), (CAST ('sgeede.com' AS text)))""")
		self._cr.execute(f"""UPDATE ir_ui_view SET arch_prev = REPLACE(arch_prev::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))""")
		self._cr.execute(f"""UPDATE ir_ui_view_custom SET arch = REPLACE(arch::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_ui_view_custom SET arch = REPLACE(arch::text, (CAST ('odoo.com' AS text)), (CAST ('sgeede.com' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE mail_template SET body_html = REPLACE(body_html::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE mail_template SET body_html = REPLACE(body_html::text, (CAST ('odoo.com' AS text)), (CAST ('sgeede.com' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE mail_template SET subject = REPLACE(subject::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE mail_template SET name = REPLACE(name::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE mail_template SET email_from = REPLACE(email_from::text, (CAST ('odoo.com' AS text)), (CAST ('sgeede.com' AS text)))""")
		self._cr.execute(f"""UPDATE res_partner SET name = REPLACE(name::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))""")
		self._cr.execute(f"""UPDATE res_partner SET email = REPLACE(email::text, (CAST ('odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))""")
		self._cr.execute(f"""UPDATE res_partner SET website = REPLACE(website::text, (CAST ('odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))""")
		self._cr.execute(f"""UPDATE res_partner SET website = REPLACE(website::text, (CAST ('odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))""")
		self._cr.execute(f"""UPDATE ir_model_fields SET help = REPLACE(help::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_model_fields SET field_description = REPLACE(field_description::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_model_fields_selection SET name = REPLACE(name::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))::jsonb""")
		self._cr.execute(f"""UPDATE ir_ui_view SET name = REPLACE(name::text, (CAST ('Odoo' AS text)), (CAST ('SGEEDE ERP' AS text)))""")


		return {
			'type': 'ir.actions.client',
			'tag': 'reload',
		}
