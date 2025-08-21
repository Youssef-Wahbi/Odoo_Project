from odoo import models, fields, api

class MyWizard(models.TransientModel):
    _name = 'my.wizard'
    _description = 'My Wizard'

    name = fields.Char(string='Name')

    @api.model
    def action_confirm(self):
        # Wizard action logic
        pass
