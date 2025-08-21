from odoo import models, fields, api

class HospitalPrescription(models.Model):
    

    
    
    _name = 'hospital.prescription'
    _description = 'Hospital Prescription'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Prescription Reference', required=True, tracking=True)
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True, tracking=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', tracking=True, readonly=True, related='patient_id.doctor_id', store=True)
    date_prescribed = fields.Date(string='Date Prescribed', default=fields.Date.context_today, tracking=True)
    medication = fields.Text(string='Medication Details', required=True)
    notes = fields.Text(string='Notes')

    treatment_id = fields.Many2one('hospital.treatment', string='Treatment', tracking=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ], string='Status', default='draft', tracking=True)

    medicine_line_ids = fields.One2many('hospital.prescription.medicine.line', 'prescription_id', string='Medicine Lines')

    def action_confirm(self):
        self.ensure_one()
        self.state = 'confirmed'
        return self._reload_action()

    def action_done(self):
        self.ensure_one()
        self.state = 'done'
        return self._reload_action()

    def action_reset_draft(self):
        self.ensure_one()
        self.state = 'draft'
        return self._reload_action()

    def _reload_action(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }

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



class HospitalPrescriptionMedicineLine(models.Model):
    _name = 'hospital.prescription.medicine.line'
    _description = 'Prescription Medicine Line'

    prescription_id = fields.Many2one('hospital.prescription', string='Prescription', required=True, ondelete='cascade')
    medicine_id = fields.Many2one('product.product', string='Medicine', required=True)
    price = fields.Float(string='Price', compute='_compute_price', store=True)

    
    dosage = fields.Char(string='Dosage')
    duration = fields.Char(string='Duration')
    notes = fields.Text(string='Notes')

    @api.depends('medicine_id')
    def _compute_price(self):
        for line in self:
            line.price = line.medicine_id.list_price if line.medicine_id else 0.0
