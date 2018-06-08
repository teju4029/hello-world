from openerp import api, models, fields, _, SUPERUSER_ID
from odoo.exceptions import ValidationError

class train_train(models.Model):
    _name = 'train.train'
    _rec_name = 'train_name'

    train_no = fields.Integer(String = 'Train No.')
    train_name = fields.Char(string = 'Train Name')
    date = fields.Date(string = 'Date')
    train_routes = fields.Many2one('train.route',string='Train Routes')
    ticket_details = fields.One2many('ticket.detail', 'train_id', 'Ticket Details')
    total = fields.Float(string='Total', compute='get_total')
    #name = fields.Char('Sequence')


    def get_total(self):
        for record in self:
            sum=0
            for val in record.ticket_details:
                if val.state == 'confirm':
                   sum+=val.subtotal
            record.total = sum

    @api.multi
    def name_get(self):
        result = []
        name = ''
        for record in self:
            if record.train_no:
                name = "[%s] %s" % (str(record.train_no),record.train_name)
                #name = str(record.train_no) + record.train_name
            else:
                name = record.train_name
            result.append((record.id,name))
        return result

    @api.model
    def name_search(self,name,args=None,operator='ilike',limit=100):
        rec = self.browse()
        print"=================SELF.BROWSE()",rec
        if name:
            print"==========name===========",name
            rec = self.search([('train_name',operator,name)] + args,limit=limit)
        if not rec:
            rec = self.search([('train_no', operator, name)] + args, limit=limit)

        return rec.name_get()

    @api.model
    def create(self,create_values):
        res = super(train_train,self).create(create_values)
        return res

    @api.multi
    def write(self,vals):
        if 'train_no' in vals and len(str(vals['train_no'])) != 5:
            raise ValidationError("Train number is not valid.")
        res = super(train_train,self).write(vals)
        return res


class ticket_detail(models.Model):
    _name = 'ticket.detail'

    name = fields.Char(string='Passenger Name')
    origin = fields.Many2one('board.details',string='Boarding Point')
    designation = fields.Many2one('desti.details', string='Destination Point')
    price = fields.Float('Price')
    total_pass_no = fields.Integer('Total Passengers')
    subtotal = fields.Float('Subtotal')
    train_id = fields.Many2one('train.train','Train')
    reservation_id = fields.Many2one('ticket.counter','Reservation')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('cancel', 'Cancel')], 'State',
                             default='draft')

    @api.onchange('price', 'total_pass_no')
    def onchange_price(self):
        if self.price and self.total_pass_no:
            self.subtotal = self.price * self.total_pass_no



    #       sales order classs...........................





class sales_order(models.Model):

    _inherit = 'sale.order'

    ref = fields.Char('Reference')
    reservation_details = fields.One2many('ticket.counter','sale_id', 'Reservation')



    def action_confirm(self):
        for order in self:
            print "==================order.reservation_details",order.reservation_details
            order.reservation_details.confirm_resservation()
            order.state = 'sale'
            order.write({'ref':self.name})
            order.confirmation_date = fields.Datetime.now()
            if self.env.context.get('send_email'):
                self.force_quotation_send()
            order.order_line._action_procurement_create()
        if self.env['ir.values'].get_default('sale.config.settings', 'auto_done_setting'):
            self.action_done()


        #self.ref = self.name
        return True








