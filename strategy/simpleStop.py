'''
Created on 2019/11/16

@author: kot
'''
from strategy import Strategy
import env
import lib.tradelib as tradelib
import lib
from tools.subchart import SubChart

class SimpleStopStrategy(Strategy):
    def __init__(self, instrument, granularity, profitpips):
        self.instrument = instrument
        self.granularity = granularity
        self.subc = None
        self.profit = tradelib.pip2Price(profitpips, instrument)
        self.unitsecs = tradelib.getUnitSecs(granularity)
        self.pipprice = tradelib.pip2Price(1, instrument)
        self.id = -1
        self.curr_side = env.SIDE_BUY
        self.now = -1
    
    def onTick(self, tickEvent):
        if self.subc == None:
            self.subc = SubChart("SimpleStop",
                                 self.instrument, 
                                 self.granularity, 
                                 endep=tickEvent.time)
        
        now = self.subc.onTick(tickEvent)
        if now == self.now:
            return []
        self.now = now
        
        orders = []
        #if lib.str2epoch("2019-11-15T00:30:00") == tickEvent.time:
        #    print(tickEvent.time)
        if self.id == -1:
            self.curr_side *= -1
            if self.curr_side == env.SIDE_BUY:
                price = tickEvent.l - self.pipprice*3
            else:
                price = tickEvent.h + self.pipprice*3
        
            order = self.createStopOrder(
                    tickEvent, self.instrument, self.curr_side, 1, 
                    price,
                    validep=tickEvent.time+self.unitsecs,
                    takeprofit=price+self.curr_side*self.profit, 
                    stoploss=price-self.curr_side*self.profit)
            if order != None:
                self.id = order.id
                orders.append(order)
            
        return orders
        
        
    def onSignal(self, signalEvent):
        if self.id == signalEvent.id:
            if signalEvent.signal in [env.ESTATUS_ORDER_CLOSED,
                                      env.ESTATUS_TRADE_CLOSED]:
                self.id = -1
        