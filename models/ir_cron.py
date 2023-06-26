from odoo import models, _
from datetime import date

class CheckOfferExpiry(models.Model):
    """ Model describing cron jobs for offer expiry date.
    """

    _name = "product.offer.expiry"
    _inherit = "product.offer"
    _description = 'Scheduled Action for checking offer expiry date'
    
    def check_offer_expiry_date(self):
        todaysDate = date.today()
        offers_list = self.env['product.offer'].search([('state','=','active')])
        
        for offer in offers_list:
            if offer.date_stop > todaysDate:
                offer.state = 'close'
                for line in offer.offer_line_ids:
                    if line.product_id:
                        line.product_id.list_price = line.old_price
                        line.product_id.on_offer = False
            else:
                pass
                