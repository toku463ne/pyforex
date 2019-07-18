'''
Created on 2019/04/20

@author: kot
'''

from strategy import Strategy
import env
import lib.tradelib as tradelib

class SimpleStrategy(Strategy):
    
    def __init__(self, instrument, profitpips):
        self.instrument = instrument
        self.profit = tradelib.pip2Price(profitpips, instrument)
        self.id = -1
        self.curr_side = env.SIDE_BUY
        self.trade_start_price = 0
    
    def onTick(self, tickEvent):
        #if self.id == 3:
        #    print("debug")
        
        if self.id == -1:
            self.curr_side *= -1
            if self.curr_side == env.SIDE_BUY:
                price = tickEvent.ask
            else:
                price = tickEvent.bid
                
            self.id = self.createOrder(tickEvent.time, self.instrument, self.curr_side, 
                             env.ORDER_MARKET, 1, price, 
                             desc="test")
            self.trade_start_price = price
            
        else:
            if self.curr_side == env.SIDE_BUY:
                price = tickEvent.bid
            else:
                price = tickEvent.ask
            if self.trade_start_price + self.profit < price or \
                self.trade_start_price - self.profit > price:
                self.closeTrade(self.id)
            
    def onSignal(self, signalEvent):
        if self.id == signalEvent.id:
            if signalEvent.signal >= env.ESIGNAL_TRADE_CLOSED:
                self.id = -1
