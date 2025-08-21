from odoo import models, fields, api

class HospitalRoom(models.Model):
    
    _name = 'hospital.room'
    _description = 'Hospital Room'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Room Number/Name', required=True, tracking=True)
    room_type = fields.Selection([
        ('general', 'General'),
        ('private', 'Private'),
        ('icu', 'ICU'),
    ], string='Room Type', required=True, tracking=True)
    capacity = fields.Integer(string='Capacity', default=1, tracking=True)
    is_available = fields.Boolean(string='Available', default=True, tracking=True)
    notes = fields.Text(string='Notes')

    patient_ids = fields.One2many('hospital.patient', 'room_id', string='Patients')

    @api.constrains('patient_ids', 'capacity')
    def _check_room_capacity(self):
        for room in self:
            if len(room.patient_ids) > room.capacity:
                raise models.ValidationError('Number of patients exceeds room capacity!')
