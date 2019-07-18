'''
Created on 2019/05/01

@author: kot
'''

from strategy import Strategy
from index.peaks import PeaksIndex

class PeakTesterStrategy(Strategy):
    
    def __init__(self, instrument, granularity, startep, endep, nbars, 
                 peak_span=5, cachesize=5, maxsize=10):
        self.peak = PeaksIndex(instrument, granularity, startep, endep, nbars, 
                 peak_span, cachesize, maxsize)
        
        
    def onTick(self, tickEvent):
        self.peak.onTick(tickEvent)
        
        