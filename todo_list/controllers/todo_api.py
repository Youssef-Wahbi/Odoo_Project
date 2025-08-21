import json
from odoo import http
from odoo.http import request


class TodoApi(http.Controller):

    def valid_response(self, message, data=None, status_code=200):
        """Helper method for valid responses"""
        response = {
            "message": message,
            "status": "success"
        }
        if data is not None:
            response["data"] = data
        return request.make_json_response(response, status=status_code)

    def invalid_response(self, message, status_code=400, data=None):
        """Helper method for invalid responses"""
        response = {
            "message": message,
            "status": "error"
        }
        if data is not None:
            response["data"] = data
        return request.make_json_response(response, status=status_code)

    @http.route('/api/todo/test', auth='none', type='http', methods=['GET'], csrf=False)
    def test(self):
        return self.valid_response('API is working!')

    #  TASK API 

    @http.route("/api/todo/task", auth='none', type='http', methods=['POST'], csrf=False)
    def create_task(self):
        try:
            data = json.loads(request.httprequest.data.decode())
            task = request.env['todo.task'].sudo().create(data)
            return self.valid_response("Task created", {
                "id": task.id,
                "name": task.name
            })
        except Exception as e:
            return self.invalid_response(str(e))

    @http.route('/api/todo/task/<int:task_id>', methods=['GET'], type='http', auth='none', csrf=False)
    def get_task(self, task_id):
        try:
            task = request.env['todo.task'].sudo().browse(task_id)
            if not task.exists():
                return self.invalid_response("Task not found", status_code=404)
            
            return self.valid_response("Task fetched", {
                "id": task.id,
                "name": task.name,
                "status": task.status,
                "description": task.description,
                "employee": task.employee_id.name if task.employee_id else None
            })
        except Exception as e:
            return self.invalid_response(str(e))

    @http.route('/api/todo/tasks', methods=["GET"], type="http", auth="none", csrf=False)
    def get_tasks(self):
        try:
            tasks = request.env['todo.task'].sudo().search([])
            result = [{
                "id": task.id,
                "name": task.name,
                "status": task.status,
                "employee": task.employee_id.name if task.employee_id else None
            } for task in tasks]
            
            return self.valid_response("Tasks fetched", {"tasks": result})
        except Exception as e:
            return self.invalid_response(str(e))

    #  EMPLOYEE API 

    @http.route("/api/todo/employee", auth='none', type='http', methods=['POST'], csrf=False)
    def create_employee(self):
        try:
            data = json.loads(request.httprequest.data.decode())
            employee = request.env['todo.employee'].sudo().create(data)
            return self.valid_response("Employee created", {
                "id": employee.id,
                "name": employee.name
            })
        except Exception as e:
            return self.invalid_response(str(e))

    @http.route('/api/todo/employees', methods=["GET"], type="http", auth="none", csrf=False)
    def get_employees(self):
        try:
            employees = request.env['todo.employee'].sudo().search([])
            result = [{
                "id": emp.id,
                "name": emp.name,
                "department": emp.department,
                "position": emp.position
            } for emp in employees]
            
            return self.valid_response("Employees fetched", {"employees": result})
        except Exception as e:
            return self.invalid_response(str(e)) 