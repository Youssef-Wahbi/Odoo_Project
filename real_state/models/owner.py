from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Owner(models.Model):
    _name = 'owner'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=1)
    phone = fields.Char()
    address = fields.Char()
    property_ids = fields.One2many('property', 'owner_id')