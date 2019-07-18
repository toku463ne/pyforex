'''
Created on 2019/04/20

@author: kot
'''
import env

class TradeEvent(object):
    def __init__(self, _id, trade_id, 
                instrument, side, units, start_price, start_time, 
                status=env.ESTATUS_TRADE_OPENED, takeprofit_price=0, stoploss_price=0,
                end_price=-1, profit=0, end_time=0, desc=""):
        self.type = env.EVETYPE_SIGNAL
        self.id = _id
        self.trade_id = trade_id
        self.status = status
        self.instrument = instrument
        self.side = side
        self.units = units
        self.start_price = start_price
        self.end_price = end_price
        self.profit = profit
        self.takeprofit_price = takeprofit_price
        self.stoploss_price = stoploss_price
        self.start_time = start_time
        self.end_time = end_time
        #self.completed = False
        self.desc = desc
        