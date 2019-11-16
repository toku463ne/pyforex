'''
Created on 2019/04/13

@author: kot
'''

from ticker import Ticker
from event.tick import TickEvent
import env

NORMAL_SPREAD = 0.4
MAX_SPREAD = 10

import lib.tradelib as tradelib
import lib.getter as getterlib
EP = 0
O = 1
H = 2
L = 3
C = 4
V = 5

class BackTestTicker(Ticker):
    def __init__(self, instrument, granularity, startep, endep, spread=NORMAL_SPREAD):
        self.prices = getterlib.getPrices(instrument, granularity, startep, endep)
        self.pos = 0
        self.now = -1 
        self.ticker_type = env.TICKTYPE_OFFLINE
        self.spread_price = tradelib.pip2Price(spread, instrument)
        
    def tick(self):
        self.pos += 1
        if self.pos >= len(self.prices[EP]):
            return None
        #(t,_,h,l,c,_) = self.dataGetter.getPriceAt(self.pos)
        t = self.prices[EP][self.pos]
        
   
        o = self.prices[O][self.pos]
        h = self.prices[H][self.pos]
        l = self.prices[L][self.pos]
        c = self.prices[C][self.pos]
        
        #import lib
        #if t >= lib.str2epoch("2019-04-01T08:20:00", 
        #                                   "%Y-%m-%dT%H:%M:%S"):
        #    print("here")
        
        
        updated = t!=self.now
        price = (h+l+c)/3
        self.now = t
        if updated:
            return TickEvent(t, price-self.spread_price/2, 
                             price+self.spread_price/2, o=o, h=h, l=l, c=c)
        else:
            return None
    
    