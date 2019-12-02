'''
Created on 2019/11/19

@author: kot
'''
from index import TechnicalIndex
import lib
import const_candles
from collections import OrderedDict
from event.info import InfoEvent


class PeakIndex(TechnicalIndex):
    #def __init__(self, instrument, granularity, 
    #             startep, endep, peaksize, peakspan):
    
    def __init__(self, subChart, peaksize, peakspan, 
                 minmax_keep_span=12*24, collectPlotInfo=False):
        super(PeakIndex, self).__init__("PeakIndex%d" % peaksize, 
                                        subChart.instrument, 
                                        subChart.granularity)
        #self.subc = SubChart("PeakIndex%d" % peakspan, 
        #                     instrument, granularity, startep, 
        #                     endep, nbars=peakspan+peaksize*2)
        self.subc = subChart
        self.peaksize = peaksize
        self.peakspan = peakspan
        self.collectPlotInfo = collectPlotInfo
        self.minmax_keep_span = minmax_keep_span
        
        self.tops = OrderedDict()
        self.bottoms = OrderedDict()
        self.top_trendlines = OrderedDict()
        self.bottom_trendlines = OrderedDict()
        self.top_trendepochs = OrderedDict()
        self.bottom_trendepochs = OrderedDict()
        self.zigzag = OrderedDict()
        self.epochs = []
        
        self.maxs = {}
        self.mins = {}
        
        self.now = self.subc.getNow()
        #self.calc(self.nowidx-peakspan, self.nowidx, self.now)
        self.calc(self.now-peakspan*self.unitsecs, self.now)
        
        
    
    def onTick(self, tickEvent):
        epoch = tickEvent.time
        _, epoch = self.subc.getTime(epoch)
        if epoch <= self.now:
            return False
        
        if not self.calc(self.now, epoch):
            return False
        
        self.now = epoch
        return True
        
        
    def calc(self, startep, endep):
        is_top_updated = False
        is_bottom_updated = False

        (t,_,h,l,_,_) = self.subc.getPrices(
            startep-self.peaksize*2*self.unitsecs, endep)
        if t[0] > startep - self.peaksize*self.unitsecs*2:
            return False
        
        def update_zigzag(isMax, lastt, lastv, ritems):
            zzitems = list(self.zigzag.items())
            if len(zzitems)>0:
                zzep, _ = zzitems[-1]
                if isMax:
                    (t, v) = self.subc.getMin(zzep, lastt)
                else:
                    (t, v) = self.subc.getMax(zzep, lastt)
            
            if len(ritems) > 0:
                ritemep, _ = ritems[-1]
                if len(zzitems) > 0 and ritemep < zzep:
                    self.zigzag[t] = v
            else:
                if len(zzitems) > 0:
                    self.zigzag[t] = v
            self.zigzag[lastt] = lastv
            
        
        for i in range(self.peaksize*2-1, len(t)):
            midi = i - self.peaksize + 1
            midh = h[midi]
            midl = l[midi]
            midt = t[midi]
            
            btitems = list(self.bottoms.items())
            tpitems = list(self.tops.items())
                    
            if midh == max(h[i-self.peaksize*2+2:i+1]):
                self.tops[midt] = midh
                is_top_updated = True
                update_zigzag(True, midt, midh, btitems)
                
            if midl == min(l[i-self.peaksize*2+2:i+1]):
                self.bottoms[midt] = midl
                is_bottom_updated = True
                update_zigzag(False, midt, midl, tpitems)
                
        
        exepoch,_,_,_,_,_ = self.subc.getBeforeNPrice(endep, 
                                            self.peakspan)
        for (peak,trendlines,trendepochs) in [
            (self.tops, self.top_trendlines, self.top_trendepochs), 
            (self.bottoms, self.bottom_trendlines, self.bottom_trendepochs)]:
            for epoch in sorted(list(peak.keys())):
                if epoch  >= exepoch:
                    break
                del peak[epoch]
                if epoch in trendlines.keys():
                    del trendlines[epoch]
                    del trendepochs[epoch]
                
                
        if is_top_updated:
            self._constructTrendlines(True)
            self._updateMaxMin(True)
        if is_bottom_updated:
            self._constructTrendlines(False)
            self._updateMaxMin(False)
            
        return True
    
    
    def getMax(self):
        mav = 0
        mat = 0
        for epoch in self.tops.keys():
            v = self.tops[epoch]
            if v > mav:
                mav = v
                mat = epoch
        return (mat, mav)
    
    
    
    def getMin(self):
        miv = 0
        mit = 0
        for epoch in self.bottoms.keys():
            v = self.bottoms[epoch]
            if v < miv or miv == 0:
                miv = v
                mit = epoch
        return (mit, miv)
    
    
    
    def _constructTrendlines(self, isTop=True):
        if isTop:
            peaks = self.tops
        else:
            peaks = self.bottoms
        trendlines = {}
        trendepochs = {}
        peak_epochs = sorted(list(peaks.keys()),reverse=True)
        base_epoch = peak_epochs.pop(0)
        for i in range(len(peak_epochs)):
            trend_epoch = peak_epochs[i]
            if base_epoch - trend_epoch < self.unitsecs*self.peaksize:
                continue
            coefficient = (peaks[base_epoch]-peaks[trend_epoch])/(base_epoch-trend_epoch)
            val = peaks[base_epoch] - coefficient*base_epoch
            is_broken = False
            for epoch in list(trendlines.keys()):
                if isTop: 
                    if val + coefficient*epoch < peaks[epoch]:
                        is_broken = True
                        break
                else:
                    if val + coefficient*epoch > peaks[epoch]:
                        is_broken = True
                        break
            if not is_broken:
                trendlines[trend_epoch] = coefficient
                trendepochs[trend_epoch] = (trend_epoch, base_epoch, self.now)
                
        if isTop:
            self.top_trendlines = trendlines
            self.top_trendepochs = trendepochs
        else:
            self.bottom_trendlines = trendlines
            self.bottom_trendepochs = trendepochs
           
           
    def _updateMaxMin(self, isMax):
        exepoch,_,_,_,_,_ = self.subc.getBeforeNPrice(self.now, 
                                            self.minmax_keep_span)
        peak_exepoch,_,_,_,_,_ = self.subc.getBeforeNPrice(self.now, 
                                            self.peakspan)
        if isMax:
            mami = self.maxs
        else:
            mami = self.mins
        
        if len(mami) > 1:
            for epoch in sorted(list(mami.keys())):
                if exepoch > epoch:
                    del mami[epoch]
                else:
                    break
        if len(mami) > 0:
            if isMax:
                last_ep = sorted(self.tops.keys())[-1]
                top = self.tops[last_ep]
                mt = sorted(self.maxs.keys())[-1]
                ma = self.maxs[mt]
                if top > ma or peak_exepoch > mt:
                    self.maxs[last_ep] = top
            else:
                last_ep = sorted(self.bottoms.keys())[-1]
                bt = self.bottoms[last_ep]
                mt = sorted(self.mins.keys())[-1]
                mi = self.mins[mt]
                if bt < mi or peak_exepoch > mt:
                    self.mins[last_ep] = bt
        else:
            if isMax:
                (ep, top) = self.getMax()
                self.maxs[ep] = top
            else:
                (ep, bt) = self.getMin()
                self.mins[ep] = bt
        
            
        
    def getPriceOnTrendlines(self, epoch, isTop):
        if isTop:
            peaks = self.tops
            trendlines = self.top_trendlines
        else:
            peaks = self.bottoms
            trendlines = self.bottom_trendlines
        
        prices = []
        for trend_epoch in sorted(list(trendlines.keys())):
            #if trend_epoch == 1574907900:
            #    print(lib.epoch2dt(1574907900))
            initial_price = peaks[trend_epoch]
            coefficient = trendlines[trend_epoch]
            prices.append(
                (trend_epoch, 
                 initial_price + coefficient*(epoch-trend_epoch),
                 coefficient))
            
        return prices
    
    
    
if __name__ == "__main__":
    startep = lib.str2epoch("2019-11-12T12:00:00")
    endep = lib.str2epoch("2019-11-12T22:00:00")
    p = PeakIndex("USD_JPY", "M5", 
                 startep, endep, 5, 48)
    print(p.tops)
    print(p.bottoms)
    
    