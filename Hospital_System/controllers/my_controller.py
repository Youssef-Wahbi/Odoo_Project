from odoo import http

class MyController(http.Controller):
    @http.route('/my_module/hello', auth='public', website=True)
    def hello(self, **kwargs):
        return "Hello, World!"
