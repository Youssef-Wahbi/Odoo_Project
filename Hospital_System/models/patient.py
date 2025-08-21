    
from odoo import models, fields

class Patient(models.Model):
   
   
    
    _name = 'hospital.patient'
    _description = 'Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    email = fields.Char(string='Email')
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    bill = fields.Float(string='Bill')
    room_id = fields.Many2one('hospital.room', string='Room')
    is_vip = fields.Boolean(string='VIP Patient')

    treatment_ids = fields.One2many('hospital.treatment', 'patient_id', string='Treatments')
    prescription_ids = fields.One2many('hospital.prescription', 'patient_id', string='Prescriptions')



    def action_create_invoice(self):
        move_obj = self.env['account.move']
        partner_obj = self.env['res.partner']
        # Find or create a default partner
        partner = partner_obj.search([('name', '=', 'Hospital Patient')], limit=1)
        if not partner:
            partner = partner_obj.create({'name': 'Hospital Patient'})
        for patient in self:
            invoice = move_obj.create({
                'move_type': 'out_invoice',
                'partner_id': partner.id,
                'invoice_origin': patient.name,
                'invoice_line_ids': [
                    (0, 0, {
                        'name': f'Patient Bill for {patient.name}',
                        'quantity': 1,
                        'price_unit': patient.bill or 0.0,
                    })
                ],
            })
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': invoice.id,
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
