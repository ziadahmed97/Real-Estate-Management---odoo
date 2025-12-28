from odoo import models,fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    property_id = fields.Many2one('property')

    def action_confirm(self):
        res = super(SaleOrder,self).action_confirm()
        print("inside action_confirm method")
        return res
    def action_do_something(self):
        print(self,"inside do something")
