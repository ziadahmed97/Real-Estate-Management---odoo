from odoo import *
class Building(models.Model):
    _name = "building"
    _description = 'building Record'
    _rec_name = 'code'
    _inherit = ['mail.thread','mail.activity.mixin']
    name =fields.Char(required=True, default='New',size=12)
    description = fields.Text()
    no =fields.Integer()
    code =fields.Char()
    active = fields.Boolean(default=True)