
import lib.tradelib as tradelib
import lib
import math
from tools.latestpricelist import LatestPriceList

class TechnicalIndex(object):
    
    
    def __init__(self, instrument, granularity, cache_len=12*24):
        self.epochs = []
        self.instrument = instrument
        self.granularity = granularity
        self.unitsecs = tradelib.getUnitSecs(granularity)
        self.latestPriceList = LatestPriceList(self.unitsecs*cache_len, 
                                               instrument)
        
    def onTick(self, tickEvent):
        pass
    
    def searchNearest(self, price):
        return self.latestPriceList.searchNearest(price)
    
    def searchObj(self, price):
        return self.latestPriceList.searchObj(price)