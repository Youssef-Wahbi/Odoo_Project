from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Employee(models.Model):
    _name = 'real.estate.employee'
    _description = 'Real Estate Employee'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Employee Name', required=True, tracking=True)
    employee_id = fields.Char(string='Employee ID', required=True, tracking=True)
    email = fields.Char(string='Email', tracking=True)
    phone = fields.Char(string='Phone', tracking=True)
    position = fields.Selection([
        ('agent', 'Real Estate Agent'),
        ('manager', 'Property Manager'),
        ('broker', 'Broker'),
        ('assistant', 'Assistant'),
        ('marketing', 'Marketing Specialist'),
        ('admin', 'Administrative Staff')
    ], string='Position', required=True, tracking=True)
    
    department = fields.Selection([
        ('sales', 'Sales'),
        ('marketing', 'Marketing'),
        ('management', 'Management'),
        ('support', 'Support'),
        ('finance', 'Finance')
    ], string='Department', tracking=True)
    
    hire_date = fields.Date(string='Hire Date', tracking=True)
    salary = fields.Monetary(string='Salary', currency_field='currency_id', tracking=True)
    currency_id = fields.Many2one('res.currency', string='Currency', 
                                 default=lambda self: self.env.company.currency_id.id)
    
    is_active = fields.Boolean(string='Active', default=True, tracking=True)
    notes = fields.Text(string='Notes')
    
    
    partner_id = fields.Many2one('res.partner', string='Contact Person', tracking=True)
    manager_id = fields.Many2one('real.estate.employee', string='Manager', tracking=True)
    property_ids = fields.One2many('property', 'agent_id', string='Assigned Properties')
    

    
    
    property_count = fields.Integer(string='Property Count', compute='_compute_property_count')
    
    @api.depends('property_ids')
    def _compute_property_count(self):
        for employee in self:
            employee.property_count = len(employee.property_ids)
    
    @api.constrains('email')
    def _check_email(self):
        for employee in self:
            if employee.email and '@' not in employee.email:
                raise ValidationError(_('Please enter a valid email address.'))
    
    @api.constrains('phone')
    def _check_phone(self):
        for employee in self:
            if employee.phone and len(employee.phone) < 10:
                raise ValidationError(_('Please enter a valid phone number.'))
    
    def action_view_properties(self):
        """Action to view assigned properties"""
        return {
            'name': _('Assigned Properties'),
            'type': 'ir.actions.act_window',
            'res_model': 'property',
            'view_mode': 'tree,form',
            'domain': [('agent_id', '=', self.id)],
            'context': {'default_agent_id': self.id},
        } 