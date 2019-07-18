'''
Created on 2019/05/06

@author: kot
'''
from ticker import Ticker
from event.tick import TickEvent

import lib.getter as getterlib
import lib

EP = 0
O = 1
H = 2
L = 3
C = 4
V = 5

class LastCandleTicker(Ticker):

    def __init__(self, instrument, granularity="M1", nbars=25):
        self.prices = getterlib.getNPrices(instrument, granularity, 
                                           lib.nowepoch(), nbars)
        self.pos = 0
        self.now = self.prices[EP][-1]
        self.instrument = instrument
        self.granularity = granularity
        
        
    def tick(self):
        self.prices = getterlib.getPrices(self.instrument, self.granularity, 
                                           self.now + 1, lib.nowepoch())
        newepoch = self.prices[EP][-1]
        if newepoch <= self.now:
            return None
        #(t,_,h,l,c,_) = self.dataGetter.getPriceAt(self.pos)
        t = self.prices[EP][-1]
        o = self.prices[O][-1]
        h = self.prices[H][-1]
        l = self.prices[L][-1]
        c = self.prices[C][-1]
        v = self.prices[V][-1]
        
        
        updated = t!=self.now
        price = (h+l+c)/3
        self.now = t
        if updated:
            return TickEvent(t, price-self.spread_price/2, 
                             price+self.spread_price/2, o=o, h=h, l=l, c=c,v=v)
        else:
            return None
    
    