'''
Created on 2019/04/14

@author: kot
'''
from event import Event
import env

#order_header = ["id", "order_id", 
#                "instrument", "side", "order_type", "units", 
#                "price", "takeprofit_price", "stoploss_price",
#                "start_time", "valid_time", "end_time", "desc"]


class OrderEvent(Event):
    def __init__(self, _id, instrument, side, order_type, units, 
                 price, takeprofit_price=0, stoploss_price=0, valid_time, desc):
        self.id = _id
        self.type = env.EVETYPE_ORDER
        self.valid_time = valid_time
        self.instrument = instrument
        self.side = side
        self.order_type = order_type
        self.units = units
        self.price = price
        self.takeprofit_price = takeprofit_price
        self.stoploss_price = stoploss_price
        self.desc = desc
        
        