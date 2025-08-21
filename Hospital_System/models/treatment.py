from odoo import models, fields, api

class HospitalTreatment(models.Model):
    
    
    _name = 'hospital.treatment'
    _description = 'Hospital Treatment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Treatment Name', required=True, tracking=True)
    description = fields.Text(string='Description')
    cost = fields.Float(string='Cost', tracking=True)
    active = fields.Boolean(string='Active', default=True)

    patient_id = fields.Many2one('hospital.patient', string='Patient', tracking=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', tracking=True, readonly=True, related='patient_id.doctor_id', store=True)
    date = fields.Date(string='Date', default=fields.Date.context_today, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ], string='Status', default='draft', tracking=True)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

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
