from odoo import models, fields

class Offer(models.Model):
    _name = 'offer'
    _description = 'Offer'

    customer_name = fields.Char(string='Customer Name', required=True)
    property_id = fields.Many2one('property', string='Property', required=True)
    amount = fields.Float(string='Amount', required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], string='Status', default='pending') 