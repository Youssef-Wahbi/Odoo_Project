
from odoo import models, fields

class Doctor(models.Model):
    
    
    
    
    _name = 'hospital.doctor'
    _description = 'Doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_ids = fields.One2many('hospital.patient', 'doctor_id', string='Patients')

    name = fields.Char(string='Name', required=True)
    specialty = fields.Selection([
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('general', 'General'),
    ], string='Specialty')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    hire_date = fields.Date(string='Hire Date')
    active = fields.Boolean(string='Active', default=True)
    nurse_id = fields.Many2one('hospital.nurse', string='Nurse')
    salary = fields.Float(string='Salary')

    image_1920 = fields.Image(string='Image', max_width=1920, max_height=1920)

    patient_count = fields.Integer(string='Patients', compute='_compute_patient_count', store=False)
    patient_list = fields.Char(string='Patient List', compute='_compute_patient_list', store=False)

    def _compute_patient_count(self):
        for doctor in self:
            doctor.patient_count = len(doctor.patient_ids)

    def _compute_patient_list(self):
        for doctor in self:
            patients = doctor.patient_ids.mapped('name')
            doctor.patient_list = ', '.join(patients)

    def action_open_nurse(self):
        self.ensure_one()
        if self.nurse_id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'hospital.nurse',
                'view_mode': 'form',
                'res_id': self.nurse_id.id,
                'target': 'current',
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'hospital.nurse',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', [])],
                'target': 'current',
            }
