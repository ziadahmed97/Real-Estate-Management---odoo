import typing

from odoo import models,fields,api
from odoo.api import ValuesType, Self
from odoo.tools import Query

from odoo18.odoo.exceptions import ValidationError


class Owner(models.Model):
    _name = "owner"
    name =fields.Char(required=True,size=12)
    phone = fields.Char(size=12)
    address=fields.Char(size=12)
    property_ids=fields.One2many('property','owner_id')
    _sql_constraints = [
        ('unique_name','unique("name")','this name exists')
    ]






