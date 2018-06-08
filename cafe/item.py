from odoo import api, fields, models, _, SUPERUSER_ID

class cafe_item (models.Model):
    _name = 'cafe.item'  # This will create table in DB called cafe.item

    _inherit = 'ticket.counter'
    
#    def total(self,cr,uid,ids,total,args=None,context=None):
#        print"ids/////////",ids
#        res={}
#        for val in self.browse(cr,uid,ids):
#            if val:
#                res[val.id]=val.qty * val.unit_price
#            else:
#                res[val.id]=0.0
#        print "res=============",res        
#        return res
        
    @api.onchange('qty','unit_price')    
    def onchange_total_price(self):
        if self.qty and self.unit_price:
            self.total_price = self.qty * self.unit_price

    def get_total(self):
        for record in self:
            sum=0
            for val in record.item_line:
                sum+=val.subtotal
            record.total = sum

        
    
    name = fields.Char(string='Name',size=128,help="Define the name of item")
    partner_id = fields.Many2one('res.partner',string='Partner')
    description = fields.Char('Description',size=128)
    unit_price = fields.Float('Unit Price')
    type = fields.Selection([('food','Food'),('drink','Drink')],string='Type')
    temp = fields.Selection([('hot','Hot'),('cold','Cold'),('any','Any')],'How Served')
    qty = fields.Float('Quantity')
    total_price = fields.Float('Total Price')
#        'total_price':fields.function(total,string='Total Price',type='float',store=True),
    state = fields.Selection([('draft','Draft'),('confirm','Confirm'),('done','Done')],'State',default='draft')
    item = fields.Selection([('tea','Tea'),('coffee','Coffee'),('other','Other')],string='Item')
    other_item = fields.Char('Other Item')
    item_line = fields.One2many('cafe.item.line','cafe_id',string='Item Lines')
    partner_ids = fields.Many2many('res.partner','cafe_partner_rel','cafe_id','partner_id',string='Partners')
    total = fields.Float(string='Total',compute='get_total')
    country_code_id = fields.Many2one('demo.orm', string='Country code')




         
        
    @api.one
    def mohit(self): 
        print"==========cr=======",self.env.cr
        print"==========uid=======",self._uid,self.env.uid
        print"==========context=======",self.env.context
        print"=============self=======",self
        print"=============id=========",self.id
        self.state = 'draft'
        self.unit_price = 10
#         self.write({'unit_price':20})
        
    @api.multi
    def confirmed(self):
        for record in self:
            record.state = 'confirm'
        
    def Done(self):
        for val in self:
            val.state = 'done'


    def create_demo_orm(self):

        if self.item_line:
            quote_lines = [(0, 0, {
                'product_id': mand_line.product_id.id,
                'qty': mand_line.qty,
                'price': mand_line.price,
                'subtotal': mand_line.subtotal,
                'cafe_id':mand_line.cafe_id.id
            }) for mand_line in self.item_line]

        vals = {
                'name':self.name,
                'partner_id':self.partner_id.id,
                'description':self.description,
                'item_line':quote_lines
        }
        res = self.env['demo.orm'].create(vals)
        print "==========================================res=============================",res
        return True



    def write_demo_orm(self):
        demos = self.env['demo.orm'].search([])
        print "========================================demos==============================",demos
        for val in demos:
            if val.country_id.name == 'India':
                val.write({'code':'+11'})
                print "=================================vals==========================",val

#    def mohit(self,cr,uid,ids,context=None):
#        return self.write(cr,uid,ids,{'state':'draft'})
#    
#     
#    def confirmed(self,cr,uid,ids,context=None):
#        return self.write(cr,uid,ids,{'state':'confirm'})
#    
#     
#    def Done(self,cr,uid,ids,context=None):
#        return self.write(cr,uid,ids,{'state':'done'})


class cafe_item_line(models.Model):
    _name='cafe.item.line'
    
    product_id = fields.Many2one('product.product','Product')
    qty = fields.Float('Quantity')
    price = fields.Float('Price')
    subtotal = fields.Float('Subtotal')
    cafe_id = fields.Many2one('cafe.item','Cafe')

    @api.onchange('qty','price')
    def onchange_subtotal(self):
        if self.qty and self.price:
            self.subtotal = self.qty * self.price



class demo_orm(models.Model):
    _name='demo.orm'
    _rec_name = 'country_id'

    name = fields.Char(string='Name', size=128, help="Define the name of item")
    partner_id = fields.Many2one('res.partner', string='Partner')
    description = fields.Char('Description', size=128)
    item_line = fields.One2many('cafe.item.line', 'cafe_id', string='Item Lines')

    country_id = fields.Many2one('res.country',string='Country Name')
    code = fields.Char(string='Code')
