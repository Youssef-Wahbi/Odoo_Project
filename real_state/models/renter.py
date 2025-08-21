from odoo import models, fields, api

class Renter(models.Model):
    _name = 'renter'
    _description = 'Renter'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Renter Name', required=True, tracking=True)
    phone = fields.Char(string='Phone', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    address = fields.Text(string='Address', tracking=True)
    id_number = fields.Char(string='ID Number', tracking=True)
    is_active = fields.Boolean(string='Active', default=True, tracking=True)
    notes = fields.Text(string='Notes')
    
    # Main relationship field
    property_id = fields.Many2one('property', string='Rented Property', tracking=True)
    
    # Rental details
    average_daily_rent = fields.Float(string='Daily Rent', readonly=False, store=True)
    rental_start_date = fields.Date(string='Rental Start Date', readonly=False, store=True)
    rental_end_date = fields.Date(string='Rental End Date', readonly=False, store=True)
    
    # Related fields from property
    property_ref = fields.Char(related='property_id.ref', string='Property Reference', store=True)
    property_name = fields.Char(related='property_id.name', string='Property Name', store=True)
    property_address = fields.Text(related='property_id.description', string='Property Address', store=True)
    
    def action_view_properties(self):
        """Action to view renter's properties"""
        return {
            'name': 'Renter Properties',
            'type': 'ir.actions.act_window',
            'res_model': 'property',
            'view_mode': 'tree,form',
            'domain': [('renter_id', '=', self.id)],
            'context': {'default_renter_id': self.id},
        }
    
    def action_create_property(self):
        """Action to select from available properties for this renter"""
        return {
            'name': 'Select Available Property',
            'type': 'ir.actions.act_window',
            'res_model': 'property',
            'view_mode': 'tree,form',
            'domain': [('renter_id', '=', False)],  # Only properties without renters
            'context': {'default_renter_id': self.id},
        } 
    
    @api.onchange('property_id')
    def _onchange_property_id(self):
        """Update rental details when property is selected"""
        if self.property_id:
            self.average_daily_rent = self.property_id.daily_rent_price
            self.rental_start_date = self.property_id.rental_start_date
            self.rental_end_date = self.property_id.rental_end_date
        else:
            self.average_daily_rent = 0.0
            self.rental_start_date = False
            self.rental_end_date = False

    @api.model
    def create(self, vals):
        """Create renter and sync with property"""
        renter = super().create(vals)
        if renter.property_id:
            # Update the property to point back to this renter
            renter.property_id.with_context(syncing_renter_property=True).write({
                'renter_id': renter.id,
            })
        return renter

    def write(self, vals):
        """Update renter and sync with property"""
        # Prevent recursion by checking context
        if self.env.context.get('syncing_renter_property'):
            return super().write(vals)
        
        # Store old property_id before update
        old_property_ids = {rec.id: rec.property_id.id for rec in self}
        
        res = super().write(vals)
        
        for rec in self:
            # If property_id changed
            if 'property_id' in vals:
                # Clear old property's renter_id if it was pointing to this renter
                old_property_id = old_property_ids.get(rec.id)
                if old_property_id and old_property_id != rec.property_id.id:
                    old_property = self.env['property'].browse(old_property_id)
                    if old_property.renter_id.id == rec.id:
                        old_property.with_context(syncing_renter_property=True).write({'renter_id': False})
                
                # Update new property to point to this renter
                if rec.property_id:
                    rec.property_id.with_context(syncing_renter_property=True).write({
                        'renter_id': rec.id,
                    })
        
        return res

    def unlink(self):
        """Remove renter and clear property reference"""
        for rec in self:
            if rec.property_id and rec.property_id.renter_id.id == rec.id:
                rec.property_id.with_context(syncing_renter_property=True).write({'renter_id': False})
        return super().unlink()