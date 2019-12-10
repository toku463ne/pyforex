'''
Created on 2019/12/08

@author: kot
'''

from index.histindex import HistIndex
import lib
from collections import OrderedDict
from event.tick import TickEvent
from tools.subchart import SubChart

class PeakIndex(HistIndex):

    def __init__(self, subChart, peaksize, peakspan, 
                 deleteOld=True, histSize=0):
        super(PeakIndex, self).__init__("PeakIndex%d" % peaksize, 
                                        subChart, histSize)
        self.subc = subChart
        self.peaksize = peaksize
        self.peakspan = peakspan
        self.deleteOld = deleteOld
        self.tops = OrderedDict()
        self.bottoms = OrderedDict()
        self.zigzag = OrderedDict()
        self.lastdir = 0
        
        self.now = self.subc.getNow()
        self.calc(self.subc.getBeforeNt(self.now, peakspan), self.now)
        
    def onTick(self, tickEvent):
        epoch = tickEvent.time
        _, epoch = self.subc.getTime(epoch)
        if epoch <= self.now:
            return False
        
        if not self.calc(self.now, epoch):
            return False
        
        self.now = epoch
        return True
    
    def topUpdated(self, epoch):
        pass
    
    def bottomUpdated(self, epoch):
        pass
    
    def peakDeleted(self, epoch, trend_epoch):
        pass
    
    
    
    def calc(self, startep, endep):
        (t,_,h,l,_,_) = self.subc.getPrices(
            startep, endep, nbars=self.peaksize*2-1)
        
        
        for i in range(self.peaksize*2-1, len(t)):
            midi = i - self.peaksize + 1
            midh = h[midi]
            midl = l[midi]
            midt = t[midi]
            epoch = t[i]
            
            if midh == max(h[i-self.peaksize*2+2:i+1]):
                self.tops[midt] = midh
                self.updateZigZag(1, midt, midh)
                self.topUpdated(epoch)
            if midl == min(l[i-self.peaksize*2+2:i+1]):
                self.bottoms[midt] = midl
                self.updateZigZag(-1, midt, midl)
                self.bottomUpdated(epoch)
            self.calcHist(epoch)
            self.deleteOldProc(epoch)
            
        return True
        
    def updateZigZag(self, newdir, newt, newv):
        zzitems = list(self.zigzag.items())
        if len(zzitems) > 0:
            oldt,(_,olddir) = zzitems[-1]
            if newdir == olddir:
                _, endt = self.subc.getTime(newt-1)
                _, startt = self.subc.getTime(oldt+self.unitsecs)
                if endt <= oldt:
                    return
                if newdir == 1:
                    (t, v) = self.subc.getMin(startt, endt)
                else:
                    (t, v) = self.subc.getMax(startt, endt)
                self.zigzag[t] = (v, -newdir)
        self.zigzag[newt] = (newv, newdir)
        olddir = newdir
        
        
    def deleteOldProc(self, lastepoch):
        exepoch,_,_,_,_,_ = self.subc.getBeforeNPrice(lastepoch, 
                                            self.peakspan)
        for peak, n in [(self.tops, 1), 
                     (self.bottoms, 2), 
                     (self.zigzag, 3)]:
            for peak_epoch in sorted(list(peak.keys())):
                if peak_epoch  >= exepoch:
                    break
                if self.deleteOld:
                    del peak[peak_epoch]
                if n in [1,2]:
                    self.peakDeleted(lastepoch, peak_epoch)
                    
            
    def getPlotElements(self, color="k"):
        epochs = []
        vals = []
        for (ep, (va, _)) in self.zigzag.items():
            epochs.append(ep)
            vals.append(va)
        from plotelement.linechart import PlotEleLineChart
        pe = PlotEleLineChart(epochs, vals, color)
        pes = [pe]
        if len(self.hist) > 0:
            pes.extend(super(PeakIndex, self).getPlotElements(color))
        return pes

def run(startep, endep, 
        instrument="USD_JPY", granularity="M5",
        peakspan=12*6, peaksize=5):
    subc = SubChart("PeakIndex",
                                 instrument, 
                                 granularity,
                                 startep=startep,
                                 endep=endep,
                                 nbars=peakspan+peaksize*2,
                                 truncateOld=False)
    p = PeakIndex(subc,peaksize, peakspan, deleteOld=False)
    tickEvent = TickEvent(endep,0,0,0)
    subc.onTick(tickEvent)
    p.onTick(tickEvent)
    return p.getPlotElements()

if __name__ == "__main__":
    instrument = "USD_JPY"
    granularity = "M5"
    startep = lib.str2epoch("2019-11-26T00:00:00")
    endep = lib.str2epoch("2019-11-29T22:00:00")
        
    pes = run(startep, endep)
    print(pes)
    
    import plotly.offline
    plotly.offline.init_notebook_mode()
    import lib.charts as m
    m.plot(instrument, granularity, 
           startep, endep, pes,datetime_display_span="h")
        