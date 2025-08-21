from odoo import models, fields

class Appointment(models.Model):
   
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Datetime(string='Date', required=True)
    reason = fields.Text(string='Reason')
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    nurse_id = fields.Many2one('hospital.nurse', string='Nurse', readonly=True, related='doctor_id.nurse_id', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='State', default='draft')

    def action_open_patient(self):
        self.ensure_one()
        if self.patient_id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'hospital.patient',
                'view_mode': 'form',
                'res_id': self.patient_id.id,
                'target': 'current',
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'hospital.patient',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', [])],
                'target': 'current',
            }

    def action_open_doctor(self):
        self.ensure_one()
        if self.doctor_id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'hospital.doctor',
                'view_mode': 'form',
                'res_id': self.doctor_id.id,
                'target': 'current',
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'hospital.doctor',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', [])],
                'target': 'current',
            }



    