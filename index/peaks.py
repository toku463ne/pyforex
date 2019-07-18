'''
Created on 2019/04/29

@author: kot
'''
from index import TechnicalIndex
from tools.subchart import SubChart
from tools.indexeddict import IndexedDict
from plotelement.peaks import PlotElePeaks
import lib

import copy

ID_MAXPEAK = "maxp"
ID_MAXPEAK_HIST = "maxph"
ID_MINPEAK = "minp"
ID_MINPEAK_HIST = "minph"

class PeaksIndex(TechnicalIndex):        
            
    def __init__(self, instrument, granularity, startep, endep=0, nbars=25, 
                 peak_span=5, cachesize=1000, 
                 collect_last_changes=False, precise=False):
        super(PeaksIndex, self).__init__(instrument, granularity)
        self.subc = SubChart(instrument, granularity, startep, 
                             endep, nbars, cachesize)
        self.nbars = nbars
        self.precise = precise
        self.collect_last_changes = collect_last_changes
        self.now = 0
        self.nowidx = 0

        
        self.maxpeaks = IndexedDict(ID_MAXPEAK)
        self.minpeaks = IndexedDict(ID_MINPEAK)
        self.spansecs = self.unitsecs * peak_span
        
        self.peak_span = peak_span
        
        (t, _, hl, ll, _, _) = self.subc.getPrices()
        self._calcPeaks(peak_span, t, hl, ll)
        
    
    def onTick(self, tickEvent):
        errret = False
        epoch = tickEvent.time
        
        i, t = self.subc.getTime(epoch)
        if t == self.now:
            return errret
        
        if i < 0:
            self.updatePeaks()
            i, _ = self.subc.getTime(epoch)
            if i < 0:
                return errret
        if i < self.nbars -1:
            return errret
        if self.now == t:
            return errret
          
        if self.maxpeaks.hasKey(i):
            p = self.maxpeaks.get(i)
            self.latestPriceList.upsert(epoch, p, p)
        if self.minpeaks.hasKey(i):
            p = self.minpeaks.get(i)
            self.latestPriceList.upsert(epoch, p, p)
        
        self.now = t
        self.nowidx = i
        return True
        
        
        
    def updatePeaks(self):
        (t, _, hl, ll, _, _) = self.subc.getPrices()
        start_idx = len(t)
        (t1, _, hl1, ll1, _, _) = self.subc.getLatestChart(t[-1])
        t.extend(t1)
        hl.extend(hl1)
        ll.extend(ll1)
        self._calcPeaks(start_idx, t, hl, ll)
        
        
    def _calcPeaks(self, start_idx, t, hl, ll):
        peak_span = self.peak_span
        for i in range(start_idx, len(t)-peak_span):
            if hl[i] == max(hl[i-peak_span:i+peak_span+1]):
                self.maxpeaks.append(i, hl[i])
                lib.printDebug(t[i], "max_peak %.3f" % hl[i])
            if ll[i] == min(ll[i-peak_span:i+peak_span+1]):
                self.minpeaks.append(i, ll[i])
                lib.printDebug(t[i], "min_peak %.3f" % ll[i])
                
        
    def truncateOldFrom(self, starti):
        nshift = self.subc.truncateOldFrom(starti)
        if nshift <= 0:
            return
        # do not consider the case idx is minus
        self.maxpeaks.shiftKeys(nshift)
        self.minpeaks.shiftKeys(nshift)
        self.nowidx -= nshift
        
    def data(self):
        return (self.maxpeaks.getData(), 
                self.minpeaks.getData())
        
    def getPrices(self):
        return self.subc.getPrices()
    
    def getPriceAt(self, idx):
        (t,o,h,l,c,v) = self.subc.getPrices()
        return t[idx],o[idx],h[idx],l[idx],c[idx],v[idx]
    
    def getPricesAt(self, starti, endi):
        if endi<starti:
            return ([],[],[],[],[],[])
        (t,o,h,l,c,v) = self.subc.getPrices()
        return (t[starti:endi+1],o[starti:endi+1],
            h[starti:endi+1],l[starti:endi+1],
            c[starti:endi+1],v[starti:endi+1])
    
    
    def getEpochs(self):
        ep,_,_,_,_,_ = self.subc.getPrices()
        return ep
        
    def getPlotElement(self, color="k"):
        (maxp, minp) = self.data()
        ep = self.getEpochs()
        pemax = PlotElePeaks(ep, maxp, True, color=color)
        pemin = PlotElePeaks(ep, minp, False, color=color)
        return [pemax, pemin]
    