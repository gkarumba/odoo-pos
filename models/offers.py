# See LICENSE file for full copyright and licensing details.

# import time
from datetime import date

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class ProductOffers(models.Model):
    '''Defines an offer.'''

    _name = "product.offer"
    _description = "Products Offers"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "sequence"
    
    # @api.model
    # def create(self, vals):
    #     vals.update({
    #         'name': self.env['ir.sequence'].next_by_code('project.timesheet')
    #     })
    #     result = super(ProductOffers, self).create(vals)
    #     for record in result:
    #         followers= []
    #         manager_partner_id = self.env['res.partner'].search([('email','=', record.manager_id.email)],limit=1)
    #         if manager_partner_id.id not in record.message_follower_ids.ids:
    #             followers.append(manager_partner_id.id)
    #         record.message_subscribe(followers)
    #     return result

    active = fields.Boolean(default=True, track_visibility='onchange')
    sequence = fields.Integer('Sequence', required=False)
    name = fields.Char('Name', required=True, help='Offer Name', track_visibility='onchange')
    date_start = fields.Date('Start Date', required=True,
                             help='Starting date of Offer', track_visibility='onchange')
    date_stop = fields.Date('End Date', required=True,
                            help='Ending Date of Offer', track_visibility='onchange')
    state = fields.Selection([('draft', 'Draft'), ('active', 'Active'), ('close', 'Closed')],
                'State',  help='State of Offer',default='draft', track_visibility='onchange')
    price = fields.Float("Price", required=True, default=0.0, track_visibility='onchange')
    offer_line_ids = fields.One2many('product.offer.line','offer_id', string="Timesheets Details")
    
    def set_active(self):
        todaysDate = date.today()
        for record in self:
            if todaysDate > record.date_stop:
                raise UserError(_("Error! You cannot activate an offer whose End Date has already elapsed"))
            elif record.date_start > todaysDate:
                raise UserError(_("Error! You cannot activate an offer whose Start Date has not started"))
            else:
                record.write({
                    'state': 'active'
                })
                for line in record.offer_line_ids:
                    if line.product_id:
                        line.old_price = line.product_id.list_price
                        line.product_id.actual_price = line.old_price
                        line.product_id.list_price = record.price
                        line.product_id.offer_price = line.offer_price
                        line.product_id.on_offer = True
                        
    def set_closed(self):
        for record in self:
            record.write({
                    'state': 'close'
                })
            for line in record.offer_line_ids:
                if line.product_id:
                    line.product_id.list_price = line.product_id.actual_price
                    line.product_id.on_offer = False
                    # line.product_id.actual_price = line.old_price
                    
    def write(self,vals):
        for record in self:
            if record.state == 'close':
                raise ValidationError(_('You can not edit an Offer, that has been closed'))
            else:
                return super(ProductOffers, self).write(vals)
            
    def unlink(self):
        for rec in self:
            try:
                if rec.state not in ['active','close']:
                    raise ValidationError(_('You can not delete an Offer, that has been closed'))
                else:
                    return super(ProductOffers, self).unlink()
            except Exception as e:
                raise ValidationError(_(f'Failed to delete, kindly reach out to Admin: {e}'))
            
    
class OffersLine(models.Model):
    '''Defines an offer line.'''

    _name = "product.offer.line"
    _description = "Products Offers line"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    @api.model
    def create(self, vals):
        product_id = vals.get('product_id')
        actual_price = self.env['product.template'].search([('id','=',product_id)]).mapped('list_price')
        vals.update({
            'old_price': actual_price[0]
        })
        return super(OffersLine, self).create(vals)

    active = fields.Boolean(default=True, track_visibility='onchange')
    offer_id = fields.Many2one('product.offer', string='Offer', required=False,tracking=True)
    name = fields.Char('Name', required=True, readonly=True,related='product_id.name', track_visibility='onchange')
    product_id = fields.Many2one('product.template', 'Product', required=True, domain="[('sale_ok', '=', True)]", track_visibility='onchange')
    old_price = fields.Float('Actual Price', required=False, readonly=True, track_visibility='onchange')
    offer_price = fields.Float('Offer Price', required=False, readonly=True, related='offer_id.price', track_visibility='onchange')
    state = fields.Selection([('draft', 'Draft'), ('active', 'Active'), ('close', 'Closed')],
                'State',  help='State of Offer',default='draft', related='offer_id.state',track_visibility='onchange')
    
    @api.onchange('product_id')
    def on_change_product_id(self):
        if not self.product_id:
            return {}
        else:
            self.write({
                'old_price': self.product_id.list_price}) 
    
    # @api.constrains('old_price')
    # def _check_old_price(self):
    #     for record in self:
    #         if record.old_price > record.offer_price:
    #             raise ValidationError("The offer price cannot be greater than the actual selling price")
            
class ProductInherit(models.Model):
    '''Defines an inherit of the product model.'''
    
    _inherit = ['product.template']
    
    on_offer = fields.Boolean('On Offer', default=False, readonly=True, track_visibility='onchange')
    offer_price = fields.Float('Offer Price', required=True, readonly=True, track_visibility='onchange')
    actual_price = fields.Float('Sale Price', required=True, readonly=True, track_visibility='onchange')