'''
Created on 2019/11/16

@author: kot
'''
from strategy import Strategy
import env
import lib.tradelib as tradelib

class SimpleMarketStrategy(Strategy):
    def __init__(self, instrument, profitpips):
        self.instrument = instrument
        self.profit = tradelib.pip2Price(profitpips, instrument)
        self.id = -1
        self.curr_side = env.SIDE_BUY
    
    def onTick(self, tickEvent):
        orders = []
        if self.id == -1:
            self.curr_side *= -1
            if self.curr_side == env.SIDE_BUY:
                price = tickEvent.ask
            else:
                price = tickEvent.bid
        
            order = self.createMarketOrder(
                    tickEvent, self.instrument, self.curr_side, 1, price,
                    takeprofit=price+self.curr_side*self.profit, 
                    stoploss=price-self.curr_side*self.profit)
            self.id = order.id
            orders.append(order)
        return orders
        
        
    def onSignal(self, signalEvent):
        if self.id == signalEvent.id:
            if signalEvent.signal in [env.ESTATUS_ORDER_CLOSED,
                                      env.ESTATUS_TRADE_CLOSED]:
                self.id = -1
        