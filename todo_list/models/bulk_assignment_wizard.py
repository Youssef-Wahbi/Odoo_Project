from odoo import models, fields, api, _


class BulkTaskAssignmentWizard(models.TransientModel):
    _name = 'bulk.task.assignment.wizard'
    _description = 'Bulk Task Assignment Wizard'

    employee_id = fields.Many2one('todo.employee', string="Assign to Employee", required=True)
    task_ids = fields.Many2many('todo.task', string="Tasks to Assign")

    @api.model
    def default_get(self, fields_list):
        """Get default values for the wizard"""
        res = super(BulkTaskAssignmentWizard, self).default_get(fields_list)
        if self.env.context.get('active_ids'):
            res['task_ids'] = [(6, 0, self.env.context.get('active_ids'))]
        return res

    def action_assign_tasks(self):
        """Assign selected tasks to the chosen employee"""
        for task in self.task_ids:
            task.employee_id = self.employee_id
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('Successfully assigned %d tasks to %s') % (len(self.task_ids), self.employee_id.name),
                'type': 'success',
            }
        } 