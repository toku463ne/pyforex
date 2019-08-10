'''
Created on 2019/08/03

@author: kot
'''

from index import TechnicalIndex
from tools.subchart import SubChart
import lib.tradelib as tradelib
import lib
from plotelement.events import PlotEleEvents
from collections import OrderedDict
from event.info import InfoEvent
import env


class MappedIndex(TechnicalIndex):
    def __init__(self, instrument, granularity, startep, endep=-1, 
                 anal_span=0, maxsize=12*24*3, map_cache_len=12*24):
        super(MappedIndex, self).__init__(instrument, granularity, map_cache_len)
        self.subc = SubChart(self.__class__.__name__, instrument, granularity, startep, 
                             endep, anal_span, maxsize)
        _, startep = self.subc.getTime(startep)
        self.now = startep - self.unitsecs
        self.anal_span = anal_span
        self.pipsize = tradelib.pip2Price(1, instrument)
        self.decimalPlace = tradelib.getDecimalPlace(instrument)
        self.data = OrderedDict()
        self.updateData(startep)

    # return map_key, map_val
    def calcData(self, subcIdx):
        pass

    
    

    def onTick(self, tickEvent):
        i, epoch = self.subc.onTick(tickEvent)
        if i == -1 or epoch == self.now :
            return 
        
        if self.now == -1:
            self.now = epoch
        
        if env.run_mode not in [env.MODE_BACKTESTING, env.MODE_UNITTEST]:
            self.updateData(self.now+self.unitsecs)
        
        curep = self.now
        while curep < epoch:
            curep += self.unitsecs
            if curep in self.data.keys():
                map_key, map_val = self.data[curep]
                self.latestPriceList.upsert(curep, map_key, map_val)
            
        self.now = epoch
    

    def updateData(self, startep=-1):
        if startep == -1:
            starti = -1
        else:
            starti, _ = self.subc.getTime(startep)
        
        (tl, _, _, _, _, _) = self.subc.getPrices()
        for i in range(starti, len(tl)):
            (map_key, map_val) = self.calcData(i)
            self.data[tl[i]] = (map_key, map_val)
        
        
        if env.run_mode not in [env.MODE_BACKTESTING, env.MODE_UNITTEST]:
            t = tl[0]
            for k in list(self.data.keys()):
                if k >= t:
                    break
                del self.data[k]
