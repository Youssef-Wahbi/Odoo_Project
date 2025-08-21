from odoo import models, fields

class Nurse(models.Model):
    
    _name = 'hospital.nurse'
    _description = 'Nurse'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    department = fields.Selection([
        ('emergency', 'Emergency'),
        ('icu', 'ICU'),
        ('surgery', 'Surgery'),
        ('pediatrics', 'Pediatrics'),
        ('general', 'General'),
    ], string='Department')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    shift = fields.Selection([
        ('morning', 'Morning'),
        ('evening', 'Evening'),
        ('night', 'Night')
    ], string='Shift')
    active = fields.Boolean(string='Active', default=True)
    salary = fields.Float(string='Salary')
    doctor_ids = fields.One2many('hospital.doctor', 'nurse_id', string='Doctors')

    image_1920 = fields.Image(string='Image', max_width=1920, max_height=1920)
