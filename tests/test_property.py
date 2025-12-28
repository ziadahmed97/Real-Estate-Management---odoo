from odoo.tests.common import TransactionCase
from odoo import *


class TestProperty(TransactionCase):
    def setUp(self,*args,**kwargs):
        super(TestProperty,self).setUp()

        self.property_01_record = self.env['property'].create(
            {
                'ref':'PRT1000',
                'name':'property73',
                'description':'sddds',
                'postcode': '54d5sd',
                'date_availability' : fields.Date.today(),
                'bedrooms' : 10
            }
        )
    def test_01_property_values(self):
        property_id = self.property_01_record
        self.assertRecordValues(property_id,[{
            'ref':'PRT1000',
                'name':'property73',
                'description':'sddds',
                'postcode': '54d5sd',
                'date_availability' : fields.Date.today(),
                'bedrooms' : 10
        }])
