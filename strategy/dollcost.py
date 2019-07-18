'''
Created on 2019/04/20

@author: kot
'''

from strategy import Strategy
import env
import lib.tradelib as tradelib

class DollCostStrategy(Strategy):
    
    def __init__(self, instrument, profitpips=30, start_unit=1, max_units=5):
        self.instrument = instrument
        self.id = -1
        self.start_unit = start_unit
        self.unit = start_unit
        self.max_units = max_units
        self.side = env.SIDE_BUY
        self.pip_price = tradelib.pip2Price(1, self.instrument)
        #self.profit = profitpips * self.pip_price
        self.profit = (profitpips/(max_units+1)) * self.pip_price
        
        
    def onTick(self, tickEvent):
        if self.id == -1:
            if self.side == env.SIDE_BUY:
                price = tickEvent.ask
            else:
                price = tickEvent.bid
                
            self.id = self.createOrder(tickEvent.time, self.instrument, self.side, 
                             env.ORDER_MARKET, self.unit, price, 
                             takeprofit_price=price+self.side*self.profit,
                             stoploss_price=price-self.side*self.profit,
                             desc="unit=%d" % self.unit)
            self.trade_start_price = price
            

    def onSignal(self, signalEvent):
        if self.id == signalEvent.id:
            if signalEvent.signal >= env.ESIGNAL_TRADE_CLOSED:
                self.id = -1
                te = signalEvent.trade_event
                if te.profit < 0:
                    self.unit += 1
                    if self.unit > self.max_units:
                        self.unit = self.start_unit
                        self.side *= -1
                else:
                    self.unit = self.start_unit
                    