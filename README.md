# odoo-pos 
A module that creates offers for products to be sold in the POS for Odoo V15


### 1- Install the Odoo POS Offers module

### 3- Access the Offers menu item from either the Purchase Module or POS module under Products menu item

### 4- Add an offer:
1. Add the name of the offer
2. Add the start date and End Date
3. Add the price for the offer
4. Add the products (```only products that can be sold```)
5. Save and Activate the Offer

### 5- Go to POS Module, products that are in the offer will have a green label
    (Offer:<name of offer>)

### 6- View the product details by clicking the info icon to view the offers details 
    original product amount and the amount saved under the offer

### 7- Pending including the Offer details in the receipt 
    Bug on reading the data rendered to the OrderReceipt, js functionality done