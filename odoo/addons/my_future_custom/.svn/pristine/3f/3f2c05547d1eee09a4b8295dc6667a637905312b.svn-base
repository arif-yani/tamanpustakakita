from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError


class WhatsAppTemplate(models.Model):
    _inherit = 'whatsapp.template'


    facebook_messager = fields.Boolean("Facebook Messager", default=False)


    @api.model
    def _find_default_for_model(self, model_name):
        res = super()._find_default_for_model(model_name)
        return self.search([
            ('model', '=', model_name),
            '|',
                ('allowed_user_ids', '=', False),
                ('allowed_user_ids', 'in', self.env.user.ids)
        ], limit=1)