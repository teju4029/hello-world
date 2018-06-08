from openerp import api, models, fields, _, SUPERUSER_ID

class train_route(models.Model):
    _name = 'train.route'
    _rec_name = 'station_name'

    station_name = fields.Char(string='Station Name')
    station_code = fields.Char(string='Station Code')



class board_details(models.Model):
    _name = 'board.details'
    _rec_name = 'b_station'

    b_station = fields.Char(string='Station Names')

class desti_details(models.Model):
    _name = 'desti.details'
    _rec_name = 'd_station'

    d_station = fields.Char(string='Station Names')


