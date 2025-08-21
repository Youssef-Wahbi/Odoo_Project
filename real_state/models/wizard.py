from odoo import models, fields, api
from odoo.exceptions import UserError

class PropertyStateWizard(models.TransientModel):
    _name = 'property.state.wizard'
    _description = 'Wizard to change state of closed property'

    property_id = fields.Many2one('property', string="Property", required=True)
    new_state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
    ], required=True)
    reason = fields.Text(string="Reason", required=True)

    def apply_change(self):
        if self.property_id.state != 'closed':
            raise UserError("Property is not in 'closed' state.")
        self.property_id.state = self.new_state
        self.property_id.message_post(body=f"State changed from Closed to {self.new_state} with reason: {self.reason}")
