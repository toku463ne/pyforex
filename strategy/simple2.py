'''
Created on 2019/04/20

@author: kot
'''

from strategy import Strategy
import env
import lib.tradelib as tradelib
from index.checker import CheckIndex

CNT_OPEN_WINDOW = 3
CNT_VALID_DENS = 3
DENSE_SIZE_PIPS = 3
NON_TRADE_HOUR_ST = 11
NON_TRADE_HOUR_ED = 14


class Simple2Strategy(Strategy):
    
    def __init__(self, instrument, granularity, profitpips, 
                 startep=-1, endep=-1):
        self.instrument = instrument
        self.profit = tradelib.pip2Price(profitpips, instrument)
        self.checker = CheckIndex(instrument, granularity, startep, endep)
        self.id = -1
        self.curr_side = env.SIDE_BUY
        self.trade_start_price = 0
    
    def onTick(self, tickEvent):
        if self.checker.onTick(tickEvent) == False:
            return
        if self.checker.isHourRange(NON_TRADE_HOUR_ST, NON_TRADE_HOUR_ED):
            return
        if not self.checker.isNHoursAfterWeekend(2):
            return
        
        if self.id == -1:
            self.curr_side *= -1
            if self.curr_side == env.SIDE_BUY:
                price = tickEvent.ask
            else:
                price = tickEvent.bid
                
            self.id = self.createOrder(tickEvent.time, self.instrument, self.curr_side, 
                             env.ORDER_MARKET, 1, price, 
                             takeprofit_price=price+self.curr_side*self.profit,
                             stoploss_price=price-self.curr_side*self.profit,
                             desc="test")
            self.trade_start_price = price
            

    def onSignal(self, signalEvent):
        if self.id == signalEvent.id:
            if signalEvent.signal >= env.ESIGNAL_TRADE_CLOSED:
                self.id = -1
