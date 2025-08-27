from odoo import models, fields

class Building(models.Model):
    _name = 'building'
    _description = 'Building'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Building Name', required=True)
    address = fields.Text(string='Address', required=True)
    total_floors = fields.Integer(string='Total Floors')
    building_type = fields.Selection([
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('mixed', 'Mixed Use'),
    ], string='Building Type', default='residential') 