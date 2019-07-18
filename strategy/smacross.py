'''
Created on 2019/04/14

@author: kot
'''

from strategy import Strategy
import lib
import lib.tradelib as tradelib
from index.sma import SmaIndex
import env

class SmaCrossStrategy(Strategy):
    def __init__(self, instrument, granularity, startep, 
                 endep=-1, sma_span=5):
        self.lastep = 0
        self.granularity = granularity
        self.unitsecs = tradelib.getUnitSecs(granularity)
        if endep == -1:
            endep = lib.nowepoch()
        self.sma = SmaIndex(instrument, granularity, startep, endep, sma_span)
        
    
    def run(self, trader, event):
        if event.type == env.EVETYPE_TICK:
            t = event.time
            if self.lastep == 0:
                self.lastep = tradelib.getNearEpoch(self.granularity, t)
            if t % self.unitsecs != 0:
                return
        
                
    
    