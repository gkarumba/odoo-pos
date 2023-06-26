from odoo import fields, models, _
from itertools import groupby
from operator import itemgetter
from datetime import date

class ProductTemplateInherit(models.Model):
    '''Defines an inherit of the product model.'''
    
    _inherit = ['product.template']
    
    on_offer = fields.Boolean('On Offer', default=False, readonly=True, track_visibility='onchange')
    offer_price = fields.Float('Offer Price', required=True, readonly=True, track_visibility='onchange')
    actual_price = fields.Float('Sale Price', required=True, readonly=True, track_visibility='onchange')
    offer_id = fields.Many2one('product.offer', string='Offer', required=False,tracking=True)
    
class ProductProductInherit(models.Model):
    _inherit = 'product.product'
    
    def get_product_info_pos(self, price, quantity, pos_config_id):
        self.ensure_one()
        config = self.env['pos.config'].browse(pos_config_id)

        # Tax related
        taxes = self.taxes_id.compute_all(price, config.currency_id, quantity, self)
        grouped_taxes = {}
        for tax in taxes['taxes']:
            if tax['id'] in grouped_taxes:
                grouped_taxes[tax['id']]['amount'] += tax['amount']/quantity if quantity else 0
            else:
                grouped_taxes[tax['id']] = {
                    'name': tax['name'],
                    'amount': tax['amount']/quantity if quantity else 0
                }

        all_prices = {
            'price_without_tax': taxes['total_excluded']/quantity if quantity else 0,
            'price_with_tax': taxes['total_included']/quantity if quantity else 0,
            'tax_details': list(grouped_taxes.values()),
            'on_offer':self.on_offer, 
            'actual_price':self.actual_price,
            'offer_price':self.offer_price,
            'saved_amount':self.actual_price - self.offer_price, 
        }

        # Pricelists
        if config.use_pricelist:
            pricelists = config.available_pricelist_ids
        else:
            pricelists = config.pricelist_id
        price_per_pricelist_id = pricelists.price_get(self.id, quantity)
        pricelist_list = [{
            'name': pl.name,
            'price': price_per_pricelist_id[pl.id]
            } for pl in pricelists]

        # Warehouses
        warehouse_list = [
            {'name': w.name,
            'available_quantity': self.with_context({'warehouse': w.id}).qty_available,
            'forecasted_quantity': self.with_context({'warehouse': w.id}).virtual_available,
            'uom': self.uom_name}
            for w in self.env['stock.warehouse'].search([])]

        # Suppliers
        key = itemgetter('name')
        supplier_list = []
        for key, group in groupby(sorted(self.seller_ids, key=key), key=key):
            for s in list(group):
                if not((s.date_start and s.date_start > date.today()) or (s.date_end and s.date_end < date.today()) or (s.min_qty > quantity)):
                    supplier_list.append({
                        'name': s.name.name,
                        'delay': s.delay,
                        'price': s.price
                    })
                    break

        # Variants
        variant_list = [{'name': attribute_line.attribute_id.name,
                         'values': list(map(lambda attr_name: {'name': attr_name, 'search': '%s %s' % (self.name, attr_name)}, attribute_line.value_ids.mapped('name')))}
                        for attribute_line in self.attribute_line_ids]
        
        all_prices['saved_amount'] = round(pricelist_list[0]['price'] - all_prices['price_with_tax'],2)

        return {
            'all_prices': all_prices,
            'pricelists': pricelist_list,
            'warehouses': warehouse_list,
            'suppliers': supplier_list,
            'variants': variant_list
        }