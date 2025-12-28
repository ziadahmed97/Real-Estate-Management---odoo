import typing

from odoo import models,fields,api
from odoo.api import ValuesType, Self
from odoo.tools import Query

from odoo18.odoo.exceptions import ValidationError


class Tag(models.Model):
    _name = "tag"
    name =fields.Char(required=True,size=12)







