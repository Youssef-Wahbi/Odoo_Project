from odoo import models, fields, api, _
from odoo.exceptions import ValidationError ,UserError
from datetime import timedelta
from datetime import date


class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'To-Do Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _translation = True

    active = fields.Boolean(default=True)
    sequence = fields.Char(string="Task Reference", readonly=True, copy=False, default=lambda self: _('New'))
    name = fields.Char(string="Task Name", required=True, translate=True)
    assign_to = fields.Many2one('res.users', string="Assign To")
    employee_id = fields.Many2one('todo.employee', string="Assigned Employee")
    description = fields.Text(string="Description", translate=True)
    due_date = fields.Date(string="Due Date")
    status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ], string="Status", default='new')
    estimated_time = fields.Float(string="Estimated Time (hours)")
    timesheet_ids = fields.One2many('todo.task.timesheet', 'task_id', string="Timesheets")

    is_overdue = fields.Boolean(string="Overdue", compute="_compute_is_overdue", store=True)

    @api.constrains('timesheet_ids')
    def _check_total_time(self):
        for task in self:
            total_time = sum(task.timesheet_ids.mapped('time_spent'))
            if task.estimated_time and total_time > task.estimated_time:
                raise ValidationError(f"Total time ({total_time}h) exceeds estimated time ({task.estimated_time}h).")

    def action_close_tasks(self):
        for task in self:
            task.status = 'completed'

    @api.depends('due_date', 'status')
    def _compute_is_overdue(self):
        today = date.today()
        for task in self:
            task.is_overdue = (
                    task.due_date and
                    task.due_date < today and
                    task.status != 'completed'
            )

    @api.model
    def create(self, vals):
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('todo_task_seq') or _('New')
        return super(TodoTask, self).create(vals)

    def action_new(self):
        """Set task status to new"""
        for task in self:
            task.status = 'new'

    def action_in_progress(self):
        """Set task status to in progress"""
        for task in self:
            task.status = 'in_progress'

    def action_completed(self):
        """Set task status to completed"""
        for task in self:
            task.status = 'completed'

    def open_assignee(self):
        """Open the assignee's form view"""
        for task in self:
            if task.assign_to:
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'res.users',
                    'res_id': task.assign_to.id,
                    'view_mode': 'form',
                    'target': 'current',
                }

    @api.model
    def cron_update_overdue_tasks(self):
        tasks = self.search([('due_date', '<', fields.Date.today()), ('status', '!=', 'completed')])
        tasks._compute_is_overdue()

    def write(self, vals):
        """Prevent editing completed tasks"""
        for task in self:
            if task.status == 'completed':
                raise UserError(_('Cannot edit completed tasks. Please change the status first.'))
        return super(TodoTask, self).write(vals)

    def action_change_status(self, new_status):
        """Change task status - used for Kanban drag and drop"""
        if new_status in ['new', 'in_progress', 'completed']:
            self.write({'status': new_status})
            return True
        return False

    def print_task_report(self):
        return self.env.ref('todo_list.action_report_todo_task').report_action(self)


class TaskTimesheet(models.Model):
    _name = 'todo.task.timesheet'
    _description = 'Task Timesheet Line'

    task_id = fields.Many2one('todo.task', string="Task", required=True, ondelete="cascade")
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user)
    time_spent = fields.Float(string="Time Spent (hours)")
    description = fields.Text(string="Description")


 
