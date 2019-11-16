'''
Created on 2019/04/20

@author: kot
'''

import env
import lib

class OrderEvent(object):
    def __init__(self, _id, cmd, epoch=0, instrument="", side=0, 
                 units=0, validep=0,
        price=0, takeprofit=0, stoploss=0, desc=""):
        self.id= _id
        self.epoch = epoch
        self.type = env.EVETYPE_ORDER
        self.instrument = instrument
        self.side = side
        self.cmd = cmd
        if cmd != env.CMD_CANCEL and _id < 0:
            raise Exception("Need id for cancel orders!")
        self.units = units
        self.validep = validep
        self.price = price
        self.status = env.ESTATUS_NONE
        self.takeprofit_price = takeprofit
        self.stoploss_price = stoploss
        self.desc = desc
        
        self.order_close_time = 0
        
        # trade part
        self.trade_start_time = 0
        self.trade_close_time = 0
        self.trade_start_price = 0
        self.trade_close_price = 0
        self.trade_profit = 0
        
    def start_trade(self, tickEvent, price, desc=""):
        self.status = env.ESTATUS_TRADE_OPENED
        self.trade_start_time = tickEvent.time
        self.trade_start_price = price
        self.desc = desc
        
    def close_trade(self, tickEvent, price, desc=""):
        self.status = env.ESTATUS_TRADE_CLOSED
        self.trade_end_time = tickEvent.time
        self.trade_end_price = price
        self.desc = desc
        
    def close_order(self, tickEvent, desc=""):
        self.status = env.ESTATUS_ORDER_CLOSED
        self.order_close_time = tickEvent.time
        self.desc = desc
        
    def check_valid(self, tickEvent):
        if tickEvent.time > self.validep:
            self.close_order("Exceeded valid time=%s" % lib.epoch2str(self.validep))

    