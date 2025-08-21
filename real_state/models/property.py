from odoo import models, fields,api
from odoo.exceptions import ValidationError ,UserError
from datetime import timedelta


class Property (models.Model):
    _name= 'property'
    _description='Property'
    _inherit= ['mail.thread','mail.activity.mixin']

    

    active = fields.Boolean(default=True)
    ref = fields.Char(default='new' ,readonly='1')
    name=fields.Char(tracking=1, translate=True)
    description= fields.Text(translate=True)
    postcode = fields.Char(translate=True)
    expected_selling_date = fields.Date(tracking=1)
    is_late=fields.Boolean()
    date_availability = fields.Date(tracking=1)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(tracking=1)
    difference = fields.Float(
        string="Price Difference",
        compute='_compute_difference')
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    photo_ids = fields.Many2many('ir.attachment', string='Photos')
    image = fields.Binary(string='Property Image', attachment=True)
    


    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed')

    ], string="Status", default='draft')

    owner_id=fields.Many2one("owner")
    agent_id = fields.Many2one('real.estate.employee', string='Assigned Agent', tracking=True)
    renter_id = fields.Many2one('renter', string='Current Renter', tracking=True)
    
    rental_start_date = fields.Date(related='renter_id.rental_start_date', string='Rental Start Date', tracking=True, store=True)
    rental_end_date = fields.Date(related='renter_id.rental_end_date', string='Rental End Date', tracking=True, store=True)
    daily_rent_price = fields.Float(related='renter_id.average_daily_rent', string='Daily Rent Price', tracking=True, store=True)
    
    
    renter_phone = fields.Char(related='renter_id.phone', readonly=True, string='Renter Phone')
    renter_email = fields.Char(related='renter_id.email', readonly=True, string='Renter Email')
    renter_address = fields.Text(related='renter_id.address', readonly=True, string='Renter Address')
    renter_name = fields.Char(related='renter_id.name', readonly=True, string='Renter Name')
    
    owner_address = fields.Char(related='owner_id.address', readonly=True, translate=True, string='Owner Address')
    owner_phone = fields.Char(related='owner_id.phone', readonly=True, translate=True, string='Owner Phone')

    create_time = fields.Datetime(string="Create Time", default=fields.Datetime.now)
    next_time = fields.Datetime(string="Next Time", compute="_compute_next_time", store=True)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'This property name already exists!')
    ]

    line_ids=fields.One2many('property.line','property_id')

    bedroom_line_ids = fields.One2many(
        'property.line', 'property_id',
         # domain=[('room_type', '=', 'bedroom')],
        string="Bedrooms",store=True,force_save=True
    )

    # living_room_line_ids = fields.One2many(
    #     'property.line', 'property_id',
    #     domain=[('room_type', '=', 'living')],
    #     string="Living Rooms",store=True,force_save=True
    # )


     

    def action_draft(self):
        for record in self:
            record.create_history_record(record.state, 'draft')
            if record.state != 'draft':
                record.state = 'draft'
        return True

    def action_pending(self):
        for record in self:
            record.create_history_record(record.state, 'pending')
            if record.state == 'draft':
                record.state = 'pending'
        return True

    def action_sold(self):
        for record in self:
            record.create_history_record(record.state, 'sold')
            if record.state != 'pending':
                raise UserError("Only pending properties can be marked as sold!")
            record.state = 'sold'
        return True

    @api.depends('expected_price', 'selling_price')
    def _compute_difference(self):
        for record in self:
            record.difference = record.selling_price - record.expected_price




    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for record in self:
            if record.bedrooms <= 0:
                raise ValidationError("Bedrooms must be greater than zero!")

    @api.model
    def create(self, vals):

        if vals.get('ref', 'New') == 'New':
            vals['ref'] = self.env['ir.sequence'].next_by_code('property_seq') or 'New'
        return super(Property, self).create(vals)

    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        res = super(Property, self)._search(domain, offset, limit, order, access_rights_uid)
        print("inside search method")
        return res

    def write(self, vals):
        """Update property and sync with renter"""
        # Prevent recursion by checking context
        if self.env.context.get('syncing_renter_property'):
            return super().write(vals)
        
        # Store old renter_id before update
        old_renter_ids = {rec.id: rec.renter_id.id for rec in self}
        
        for record in self:
            old_state = record.state
            res = super(Property, record).write(vals)
            new_state = record.state

            if 'state' in vals and old_state != new_state:
                record.create_history_record(old_state, new_state)
            
            # Handle renter relationship changes - only sync renter_id, not rental details
            if 'renter_id' in vals:
                # Clear old renter's property_id if it was pointing to this property
                old_renter_id = old_renter_ids.get(record.id)
                if old_renter_id and old_renter_id != record.renter_id.id:
                    old_renter = self.env['renter'].browse(old_renter_id)
                    if old_renter.property_id.id == record.id:
                        old_renter.with_context(syncing_renter_property=True).write({'property_id': False})
                
                # Update new renter to point to this property
                if record.renter_id:
                    record.renter_id.with_context(syncing_renter_property=True).write({
                        'property_id': record.id,
                    })

        return res

    def unlink(self):
        """Remove property and clear renter reference"""
        for rec in self:
            if rec.renter_id and rec.renter_id.property_id.id == rec.id:
                rec.renter_id.with_context(syncing_renter_property=True).write({'property_id': False})
        res = super(Property, self).unlink()
        print("inside unlink method")
        return res

    def action_closed(self):

        for record in self:
            record.create_history_record(record.state,'closed')
            record.state = 'closed'

    @api.depends('create_time')
    def _compute_next_time(self):
        for record in self:
            if record.create_time:
                record.next_time = record.create_time + timedelta(days=7) 
            else:
                record.next_time = False

    @api.model
    def check_expected_selling_date(self):
        properties = self.search([])
        for rec in properties:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True
            else:
                rec.is_late = False

    def create_history_record(self, old_state, new_state):

        self.env['property.history'].create({
            'user_id': self.env.uid,
            'property_id': self.id,
            'old_state': old_state,
            'new_state': new_state,

        })

    def open_state_wizard(self):
        return {
            'name': 'Reopen Property',
            'type': 'ir.actions.act_window',
            'res_model': 'property.state.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_property_id': self.id
            }
        }

    def open_owner(self):
        self.ensure_one()
        if not self.owner_id:
            raise UserError("No owner set for this property.")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Owner',
            'res_model': 'owner',
            'res_id': self.owner_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_compare_properties(self):
        """Action to compare selected properties"""
        if len(self) < 2:
            raise UserError("Please select at least 2 properties to compare.")
        
        return {
            'name': 'Property Comparison',
            'type': 'ir.actions.act_window',
            'res_model': 'property.comparison.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_property_ids': [(6, 0, self.ids)]}
        }



    def action_duplicate_property(self):
        """Duplicate property action"""
        self.ensure_one()
       
        new_property = self.copy({
            'name': f'{self.name} (Copy)',
            'ref': 'new',  
            'state': 'draft',  
            'selling_price': 0,  
            'is_late': False, 
        })
        
        return {
            'name': f'Duplicated Property - {new_property.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'property',
            'res_id': new_property.id,
            'view_mode': 'form',
            'target': 'current',
        }



    def action_create_invoice(self):
       
        if not self:
            raise UserError("Please select at least one property to invoice.")

        
        product = self.env['product.product'].search([('name', '=', 'Property Sale')], limit=1)
        if not product:
            product = self.env['product.product'].create({
                'name': 'Property Sale',
                'type': 'service',
                'list_price': 0.0,
                'standard_price': 0.0,
                'detailed_type': 'service',  # Required field
            })

        
        default_tax = self.env['account.tax'].search([
            ('type_tax_use', '=', 'sale'),
            ('company_id', '=', self.env.company.id)
        ], limit=1)

        
        invoice_lines = []
        for prop in self:
            if not prop.owner_id:
                raise UserError(f"Property {prop.name} has no owner set!")
                
            invoice_lines.append((0, 0, {
                'product_id': product.id,
                'name': f"Property: {prop.name or ''}",
                'quantity': 1.0,
                'price_unit': prop.selling_price or 0.0,
                'tax_ids': [(6, 0, [default_tax.id])] if default_tax else False,
            }))

        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_move_type': 'out_invoice',
                'default_partner_id': self[0].owner_id.id,  
                'default_invoice_line_ids': invoice_lines,
            }
        }

    def action_create_sale_order(self):
        """Create a Sales Order and Invoice for selected properties"""
        if not self:
            raise UserError("Please select at least one property to create a sales order.")

        
        product = self.env['product.product'].search([('name', '=', 'Property Sale')], limit=1)
        if not product:
            product = self.env['product.product'].create({
                'name': 'Property Sale',
                'type': 'service',
                'list_price': 0.0,
                'standard_price': 0.0,
                'detailed_type': 'service',
            })

        
        order_lines = []
        for prop in self:
            if not prop.owner_id:
                raise UserError(f"Property {prop.name} has no owner set!")

            order_lines.append((0, 0, {
                'product_id': product.id,
                'name': f"Property: {prop.name or ''}",
                'product_uom_qty': 1.0,
                'price_unit': prop.selling_price or 0.0,
            }))

        
        sale_order = self.env['sale.order'].create({
            'partner_id': self[0].owner_id.id,
            'order_line': order_lines,
        })

        #  (changes state to 'sale')
        sale_order.action_confirm()

        
        invoice = sale_order._create_invoices()
        invoice.action_post()

        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
            'target': 'current',
        }









class PropertyLine(models.Model):
    _name = 'property.line'
    _description = 'Property Room/Section'

    property_id = fields.Many2one('property', string="Property")
    room_type = fields.Selection([
        ('bedroom', 'Bedroom'),
        ('living', 'Living Room'),
        ('other', 'Other'),
    ], string="Room Type", default='other')

    area = fields.Float(string="Area (m²)")
    description = fields.Char(string="Description", translate=True)

