from odoo import models, fields,api
from odoo.exceptions import ValidationError ,UserError


class PropertyHistory(models.Model):
    _name = 'property.history'
    _description = 'Property State History'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    user_id = fields.Many2one('res.users', string="Changed By")
    property_id = fields.Many2one('property', string="Property")
    old_state = fields.Char()
    new_state = fields.Char()

    bedroom_line_ids = fields.One2many(
        related='property_id.bedroom_line_ids',
        comodel_name='property.line',
        string='Bedrooms',
        readonly=True
    )