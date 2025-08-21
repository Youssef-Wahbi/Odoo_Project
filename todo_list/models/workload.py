from odoo import models, fields, tools


class UserWorkload(models.Model):
    _name = 'user.workload'
    _description = 'Employee Workload Statistics'
    _auto = False
    _rec_name = 'employee_name'

    id = fields.Integer(string='ID', readonly=True)
    employee_id = fields.Many2one('todo.employee', string="Employee", readonly=True)
    employee_name = fields.Char(string="Employee Name", readonly=True)
    total_tasks = fields.Integer(string="Total Tasks", readonly=True)
    new_tasks = fields.Integer(string="New Tasks", readonly=True)
    in_progress_tasks = fields.Integer(string="In Progress Tasks", readonly=True)
    completed_tasks = fields.Integer(string="Completed Tasks", readonly=True)
    overdue_tasks = fields.Integer(string="Overdue Tasks", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                SELECT 
                    e.id as id,
                    e.id as employee_id,
                    e.name as employee_name,
                    COUNT(t.id) as total_tasks,
                    COUNT(CASE WHEN t.status = 'new' THEN 1 END) as new_tasks,
                    COUNT(CASE WHEN t.status = 'in_progress' THEN 1 END) as in_progress_tasks,
                    COUNT(CASE WHEN t.status = 'completed' THEN 1 END) as completed_tasks,
                    COUNT(CASE WHEN t.is_overdue = true THEN 1 END) as overdue_tasks
                FROM todo_employee e
                LEFT JOIN todo_task t ON e.id = t.employee_id
                WHERE e.is_active = true
                GROUP BY e.id, e.name
                ORDER BY total_tasks DESC
            )
            """
        )


