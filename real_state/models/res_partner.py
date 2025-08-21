from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_property_new = fields.Many2one('property', string='Property', required=False)
    x_prices = fields.Float(related='x_property_new.selling_price', string='Property Price', readonly=True)
