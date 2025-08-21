from odoo import models, fields, api
from odoo.exceptions import UserError


class PropertyComparisonWizard(models.TransientModel):
    _name = 'property.comparison.wizard'
    _description = 'Property Comparison Wizard'

    property_ids = fields.Many2many('property', string='Properties to Compare')

    def action_compare_properties(self):
        """Action to compare selected properties"""
        if len(self.property_ids) < 2:
            raise UserError("Please select at least 2 properties to compare.")
        
        return {
            'name': 'Property Comparison',
            'type': 'ir.actions.act_window',
            'res_model': 'property.comparison.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_property_ids': [(6, 0, self.property_ids.ids)]}
        } 