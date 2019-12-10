
import lib.tradelib as tradelib
import lib
import math

class TechnicalIndex(object):
    
    
    def __init__(self, name, subChart):
        self.name = name
        self.instrument = subChart.instrument
        self.granularity = subChart.granularity
        self.unitsecs = tradelib.getUnitSecs(self.granularity)
        self.now = -1
        
        
    def onTick(self, tickEvent):
        epoch = tickEvent.time
        _, epoch = self.subc.getTime(epoch)
        if epoch == self.now:
            return False

        self.now = epoch
        return True
        
    
    def getPlotElement(self, color="k"):
        return None
    
    def getPlotElements(self, color="k"):
        return []
    
