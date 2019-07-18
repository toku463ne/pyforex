'''
Created on 2019/04/20

@author: kot
'''

from strategy import Strategy
import env
from index.peaks import PeakIndex

class TrailPeaksStrategy(Strategy):
    
    def __init__(self, instrument, startep, endep,
                 peakdefs=[
                     {"granularity": "M5", "nbars": 12*24, "peak_span": 5},
                     {"granularity": "H1", "nbars": 5*24, "peak_span": 5},
                     ],
                 price_diff_percentage=95):
        for peakdef in peakdefs:    
            self.peak = PeakIndex(instrument, peakdef["granularity"], 
                        startep, endep, peakdef["nbars"], peakdef["peak_span"])
        
        self.price_diff_percentage = price_diff_percentage
        
    
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
                             takeprofit_price=price+self.curr_side*self.profit,
                             stoploss_price=price-self.curr_side*self.profit,
                             desc="test")
            self.trade_start_price = price
            

    def onSignal(self, signalEvent):
        if self.id == signalEvent.id:
            if signalEvent.signal >= env.ESIGNAL_TRADE_CLOSED:
                self.id = -1
