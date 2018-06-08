from openerp import api, models, fields, _, SUPERUSER_ID

class ticket_counter(models.Model):
    _name = 'ticket.counter'

    name = fields.Char(string='Passenger Name')
    age = fields.Integer('Age')
    gender = fields.Selection([('male','Male'),('female','Female'),('other','Other')],'Gender',default='male')
    origin = fields.Many2one('board.details',string='Boarding Point')
    designation = fields.Many2one('desti.details',string='Destination Point')
    price = fields.Float('Ticket Cast')
    total_pass_no = fields.Integer('Total Passengers')
    subtotal = fields.Float('Total Cast')
    train_times = fields.Many2one('train.train',string='Train Details')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('cancel', 'Cancel')], 'State', default='draft')
    number = fields.Char('Number')
    sale_id = fields.Many2one('sale.order', 'Sales')
    reservation_id = fields.Many2one('ticket.counter', 'Reservation')




    @api.onchange('price','total_pass_no')

    def onchange_price(self):
        if self.price and self.total_pass_no:
            self.subtotal = self.price * self.total_pass_no



    @api.multi
    def cancel_reservation(self):
        for val in self:
            val.state = 'cancel'
            td_ids = self.env['ticket.detail'].search([('reservation_id','=',val.id)])
            td_ids.write({'state':'cancel'})




    def confirm_resservation(self):
        for val in self:
            seq = self.env['ir.sequence'].next_by_code('ticket.reservation')

            val.write({'state':'confirm','number':seq})
            td_vals = {'name':val.name,
                    'total_pass_no':val.total_pass_no,
                    'price':val.price,
                    'subtotal':val.subtotal,
                    'train_id':val.train_times.id,
                    'reservation_id':val.id,
                    'state':val.state,
                    }
            self.env['ticket.detail'].create(td_vals)












