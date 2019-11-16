
import lib.tradelib as tradelib
import lib
import math

class TechnicalIndex(object):
    
    
    def __init__(self, instrument, granularity, cache_len=12*24):
        self.instrument = instrument
        self.granularity = granularity
        self.unitsecs = tradelib.getUnitSecs(granularity)
        
    def onTick(self, tickEvent):
        pass
    
    def getPlotElement(self, color="k"):
        return None
    
    def getPlotElements(self, color="k"):
        return []
    
