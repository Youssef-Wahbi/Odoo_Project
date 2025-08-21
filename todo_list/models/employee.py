from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Employee(models.Model):
    _name = 'todo.employee'
    _description = 'Employee'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    

    name = fields.Char(string="Employee Name", required=True)
    employee_code = fields.Char(string="Employee Code", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    email = fields.Char(string="Email", translate=True)
    phone = fields.Char(string="Phone", translate=True)
    department = fields.Selection([
        ('it', 'IT'),
        ('hr', 'HR'),
        ('finance', 'Finance')
    ], string="Department", required=True)
    position = fields.Selection([
        ('junior', 'Junior'),
        ('senior', 'Senior'),
        ('manager', 'Manager')
    ], string="Position", required=True)
    hire_date = fields.Date(string="Hire Date")
    salary = fields.Float(string="Salary")
    is_active = fields.Boolean(string="Active", default=True)
    
    # Related user for system access
    user_id = fields.Many2one('res.users', string="Related User", help="Link to system user if needed")
    
    # Task assignment
    task_ids = fields.One2many('todo.task', 'employee_id', string="Assigned Tasks")
    task_count = fields.Integer(string="Task Count", compute="_compute_task_count")
    
    @api.depends('task_ids')
    def _compute_task_count(self):
        for employee in self:
            employee.task_count = len(employee.task_ids)
    
    @api.model
    def create(self, vals):
        if vals.get('employee_code', _('New')) == _('New'):
            vals['employee_code'] = self.env['ir.sequence'].next_by_code('todo.employee_seq') or _('New')
        return super(Employee, self).create(vals)
    
    def action_view_tasks(self):
        """Open the tasks assigned to this employee"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Tasks'),
            'res_model': 'todo.task',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {'default_employee_id': self.id},
        } 