from openerp import api, models, fields, _,SUPERUSER_ID

class wiz_demo(models.Model):
    _name = 'wiz.demo'

    name = fields.Char(string = 'Name')
    date = fields.Date('Date', default=fields.Date.context_today)
    qty = fields.Float('Quantity')
    total_price = fields.Float('Total Price')

    

