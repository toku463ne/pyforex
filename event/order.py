'''
Created on 2019/04/20

@author: kot
'''

import env

class OrderEvent(object):
    def __init__(self, _id, order_id, 
                instrument, side, order_type, units, price, 
                start_time, status=env.ESTATUS_ORDER_OPENED, 
                takeprofit_price=-1, stoploss_price=1,
                valid_time=0, end_time=0, desc=""):
        self.type = env.EVETYPE_ORDER
        self.id = _id
        self.order_id = order_id
        self.instrument = instrument
        self.side = side
        self.order_type = order_type
        self.units = units
        self.price = price
        self.status = status
        self.takeprofit_price = takeprofit_price
        self.stoploss_price = stoploss_price
        self.start_time = start_time
        self.valid_time = valid_time
        self.end_time = end_time
        self.desc = desc
        self.trade_id = -1
        
    