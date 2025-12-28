import typing


from odoo import models,fields,api
from odoo.api import Self



from odoo18.odoo.exceptions import ValidationError
from datetime import timedelta
import requests

class Property(models.Model):
    _name = "property"
    _description = 'Property'
    _inherit = ['mail.thread','mail.activity.mixin']
    ref = fields.Char(default='New',readonly=True)
    name =fields.Char(required=True, default='New')
    description = fields.Text(tracking=1)
    postcode = fields.Char(required=True)
    date_availability = fields.Date(tracking=1)
    expected_selling_date = fields.Date()
    is_late = fields.Boolean()
    date_time = fields.Datetime()
    create_time = fields.Datetime(default=fields.Datetime.now())
    next_time = fields.Datetime(compute='_compute_next_time')
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff',store = 1,readonly=True)
    bedrooms = fields.Integer()
    garage = fields.Boolean(groups = "AppOne.property_manager_group")
    garden_orientation = fields.Selection([
        ('north','North'),
        ('south','South'),
        ('west','West'),
        ('east','East')
    ],default = 'north')
    active = fields.Boolean(default=True)

    owner_id = fields.Many2one('owner')
    tag_ids= fields.Many2many('tag')

    owner_phone = fields.Char(related='owner_id.phone',readonly=False)
    owner_address = fields.Char(related='owner_id.address',readonly=False)

    line_ids= fields.One2many('property.line','property_id')

    state= fields.Selection([
        ('draft','Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed','Closed')
    ],default='draft')

    _sql_constraints = [
        ('unique_name','unique("name")','this name exists!'),
    ]

    @api.constrains('bedrooms')
    def bedroom_greater_than_zero(self):
        # for rec in self:
        for rec in self:
        # if self.bedrooms <= 0 :
            if rec.bedrooms <= 0 :
                raise ValidationError('please add valid number of bedrooms!')


    # CRUD operations
    @api.model_create_multi
    def create(self, vals_list) -> Self:
        res = super(Property,self).create(vals_list)
        #logic
        if res.ref == 'New':
           res.ref= self.env['ir.sequence'].next_by_code('property_sequence')
        return res
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None) -> Query:
    #     res = super(Property, self)._search(domain, offset=0, limit=None, order=None)
    #     return res
    @api.model
    def write(self, vals) -> typing.Literal[True]:
        res=super(Property, self).write(vals)
        return res
    def unlink(self):
        res=super(Property,self).unlink()
        return res

    def action_draft(self):
        for rec in self:
            print("draft")
            rec.create_history_record(rec.state,'draft')
            # rec.state= 'draft'
            rec.write(
                {
                    'state':'draft'
                }
            )


    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state, 'pending')
            rec.write({
                'state':'pending'
            })
    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold')
            rec.write({
                'state':'sold'
            })

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            rec.write({
                'state':'closed'
            })
    def action(self):
        # print(self.env['owner'].create(
        #     {
        #         'name':'name1',
        #         'phone':'12323'
        #     }
        # ))

        print(self.env['property'].search(['!',('name','=','siuuuuuuuu'),('postcode','=','s')]).mapped('name')) #should be all true talking about tuples

    def check_expected_selling_date(self):
        property_ids=self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True
    def action_open_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('AppOne.owner_action')
        view_id = self.env.ref('AppOne.owner_view_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id,'form']]
        return action

    @api.depends('create_time')
    def _compute_next_time(self):
        for rec in self:
            if rec.create_time :
                rec.next_time = rec.create_time + timedelta(hours=6)
            else:
                rec.next_time = False
    @api.depends('expected_price','selling_price')
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price
    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            return {
                'warning':{
                    'title':'Warning','message':'negative value','type':'notification'
                }
            }
    def create_history_record(self,old_state,new_state,reason=""):
        for rec in self:
            rec.env['property.history'].create({
                'user_id' : rec.env.uid,
                'property_id' : rec.id,
                'old_state' : old_state,
                'new_state' : new_state,
                'reason' : reason or "",
                'line_ids' : [(0,0,{'description': line.description,'area':line.area}) for line in rec.line_ids],
            })
    def action_open_change_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('AppOne.change_state_action')
        action['context']={'default_property_id':self.id}
        return action
    def property_xlsx_report(self):
        return{
            'type':'ir.actions.act_url',
            'url' : f'/property/excel/report/{self.env.context.get("active_ids")}',
            'target' : 'new'
        }
    def get_properties(self):
        payload=dict()
        try:
            response=requests.get('http://localhost:8069/v1/properties',data=payload)
            if response.status_code == 200:
                data = response.json()
                # print(data['data'][0]['bedrooms'])
                properites = data['data']
                for prop in properites:
                    print(f"property: {prop['name']}")
            else:
                pass
        except Exception as error:
            raise ValidationError(str(error))

class PropertyLine(models.Model):
    _name = 'property.line'

    area=fields.Float()
    description = fields.Char()
    property_id =fields.Many2one('property')