'''
Created on 2019/04/29

@author: kot
'''
from index import TechnicalIndex
from tools.subchart import SubChart
import lib.tradelib as tradelib
import lib
from plotelement.events import PlotEleEvents
from tools.indexeddict import IndexedDict
from event.info import InfoEvent

class DensityIndex(TechnicalIndex):
    class Block():
        def __init__(self, epoch, density, std, mean):
            self.epoch = epoch
            self.density = density
            self.std = std
            self.mean = mean
            
            
    def __init__(self, instrument, granularity, startep, endep=0, 
                 anal_span=5, cachesize=1000):
        super(DensityIndex, self).__init__(instrument, granularity)
        self.subc = SubChart(instrument, granularity, startep, 
                             endep, anal_span, cachesize)
        self.now = -1
        self.nowidx = 0
        self.anal_span = anal_span
        self.decimalPlace = tradelib.getDecimalPlace(instrument)
        self.densdata = IndexedDict("densdata")
        (t, _, hl, ll, cl, _) = self.subc.getPrices()
        self._calcDensity(anal_span, t, hl, ll, cl)
        

        
    def onTick(self, tickEvent):
        epoch = tickEvent.time
        errret = (-1,-1)
        i, t = self.subc.getTime(epoch)
        if t == self.now:
            return errret
        
        if i < 0:
            self.updateDensity()
            i, t = self.subc.getTime(epoch)
            if i < 0:
                return errret
        
        if self.densdata.hasKey(t):
            block = self.densdata.get(t)
            self.latestPriceList.upsert(epoch, block.mean, block)
        
        self.now = t
        self.nowidx= i
        
        return True
        
    def getCandle(self, i=0):
        j = self.nowidx - i
        (tl, ol, hl, ll, cl, vl) = self.subc.getPrices()
        return (tl[j],ol[j],hl[j],ll[j],cl[j],vl[j])
    

    def updateDensity(self):
        (tl, _, hl, ll, cl, _) = self.subc.getPrices()
        start_idx = len(tl)
        (t1, _, hl1, ll1, cl1, _) = self.subc.getLatestChart(tl[-1])
        tl.extend(t1)
        hl.extend(hl1)
        ll.extend(ll1)
        cl.extend(cl1)
        self._calcDensity(start_idx, tl, hl, ll, cl)
        
        
    def _calcDensity(self, start_idx, tl, hl, ll, cl):
        anal_span = self.anal_span
        for i in range(start_idx, len(tl)):
            hl_c_rate,c_mean,hl_std = tradelib.getDensity(hl[i-anal_span:i+1], 
                                                    ll[i-anal_span:i+1], 
                                                    cl[i-anal_span:i+1])
            c_mean = lib.truncFromDecimalPlace(c_mean, self.decimalPlace)
            self.densdata.append(tl[i], self.Block(tl[i],hl_c_rate,hl_std, c_mean))
        
    def truncateOldFrom(self, starti):
        nshift = self.subc.truncateOldFrom(starti)
        if nshift <= 0:
            return
        self.densdata.shiftKeys(nshift)
        self.nowidx -= nshift
        
        
    def data(self):
        return self.densdata
    
    def getPlotElement(self, color="k"):
        infoevents = []
        for ep in self.densdata.keys:
            block = self.densdata.get(ep)
            if block.density >= 0.8:
                infoevents.append(InfoEvent(ep , block.mean,
                                "density:\n %.3f" % block.density,
                                color=color))
        return PlotEleEvents(infoevents)
    