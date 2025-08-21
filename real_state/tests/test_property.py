from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestProperty(TransactionCase):
    """Simple test cases for Property model"""

    def setUp(self):
        super(TestProperty, self).setUp()
       
        self.owner = self.env['owner'].create({
            'name': 'Test Owner',
            'phone': '+1234567890',
            'address': '123 Test Street'
        })

    def test_property_creation(self):
        
        property_obj = self.env['property'].create({
            'name': 'Test Property',
            'expected_price': 100000.0,
            'owner_id': self.owner.id
        })
        
        self.assertEqual(property_obj.name, 'Test Property')
        self.assertEqual(property_obj.expected_price, 100000.0)
        self.assertEqual(property_obj.state, 'draft')
        self.assertTrue(property_obj.ref.startswith('New'))

    def test_property_state_transition(self):
       
        property_obj = self.env['property'].create({
            'name': 'Test Property',
            'expected_price': 100000.0,
            'owner_id': self.owner.id
        })
        
        
        property_obj.action_pending()
        self.assertEqual(property_obj.state, 'pending')
        
        
        property_obj.action_sold()
        self.assertEqual(property_obj.state, 'sold')

    def test_property_constraint(self):
        
        with self.assertRaises(ValidationError):
            self.env['property'].create({
                'name': 'Invalid Property',
                'expected_price': 100000.0,
                'bedrooms': 0,  
                'owner_id': self.owner.id
            }) 