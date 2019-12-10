'''
Created on 2019/12/09

@author: kot
'''
from index.peaks import PeakIndex
import const_candles
import lib
from collections import OrderedDict
from event.history import HistEvent

class TrendLinesIndex(PeakIndex):
    
    def __init__(self, subChart, peaksize, peakspan, analspan,
                 minmax_keep_span=12*24, deleteOld=True, histSize=12*3):
        self.analspan = analspan
        self.minmax_keep_span = minmax_keep_span
        self.top_trendlines = OrderedDict()
        self.bottom_trendlines = OrderedDict()
        self.top_trendepochs = OrderedDict()
        self.bottom_trendepochs = OrderedDict()
        self.maxs = {}
        self.mins = {}
        super(TrendLinesIndex, self).__init__(subChart, 
                peaksize, peakspan, deleteOld, histSize)
        
        
        

    def getIndexID(self, index_type, line_epoch):
        return "%d_%d" % (index_type, line_epoch)
    
    def getPriceOnTrendlines(self, epoch, isTop):
        if isTop:
            peaks = self.tops
            trendlines = self.top_trendlines
        else:
            peaks = self.bottoms
            trendlines = self.bottom_trendlines
        
        prices = []
        for trend_epoch in sorted(list(trendlines.keys())):
            bardiff = self.subc.getBarDiff(trend_epoch, epoch)
            if bardiff > self.peakspan:
                del trendlines[trend_epoch]
                continue
            
            #if trend_epoch == 1574907900:
            #    print(lib.epoch2dt(1574907900))
            initial_price = peaks[trend_epoch]
            coefficient = trendlines[trend_epoch]
            data = {"coeff": coefficient, "bardiff": bardiff}
            prices.append(
                (trend_epoch, 
                 initial_price + coefficient*(epoch-trend_epoch),
                 data))
            
        return prices
    
    def getMax(self):
        mav = 0
        mat = 0
        for epoch in self.tops.keys():
            v = self.tops[epoch]
            if v > mav:
                mav = v
                mat = epoch
        return (mat, mav, 1)
    
    def getMin(self):
        miv = 0
        mit = 0
        for epoch in self.bottoms.keys():
            v = self.bottoms[epoch]
            if v < miv or miv == 0:
                miv = v
                mit = epoch
        return (mit, miv, -1)
    
    def topUpdated(self, epoch):
        self._constructTrendlines(epoch, True)
        self._updateMaxMin(epoch, True)
    
    def bottomUpdated(self, epoch):
        self._constructTrendlines(epoch, False)
        self._updateMaxMin(epoch, False)
    
    def peakDeleted(self, epoch, peak_epoch):
        for p in [
            self.top_trendlines,
            self.bottom_trendlines,
            self.top_trendepochs,
            self.bottom_trendepochs,
            self.maxs,
            self.mins]:
            if peak_epoch in p.keys():
                del p[peak_epoch]
            
    
    
    def calcHistBasePrices(self, epoch):
        tprices = self.getPriceOnTrendlines(epoch, True)
        bprices = self.getPriceOnTrendlines(epoch, False)
        maxs = self.maxs.items()
        mins = self.mins.items()
        
        hes = []
        for (items, 
                index_type, color) in [
            (tprices, const_candles.LINE_TPTREND, "b"),
            (bprices, const_candles.LINE_BTTREND, "r"),
            (maxs, const_candles.LINE_MAX, "g"),
            (mins, const_candles.LINE_MIN, "orange")]:
            if items == None or len(items) == 0:
                continue
            
            for item in items:
                if index_type in [const_candles.LINE_TPTREND, 
                                  const_candles.LINE_BTTREND]:
                    (trend_epoch, price, data) = item
                elif index_type == const_candles.LINE_MAX:
                    (trend_epoch, price) = item
                    bardiff = self.subc.getBarDiff(trend_epoch, epoch)
                    data = {"bardiff": bardiff}
                elif index_type == const_candles.LINE_MIN:
                    (trend_epoch, price) = item
                    bardiff = self.subc.getBarDiff(trend_epoch, epoch)
                    data = {"bardiff": bardiff}
                else:
                    raise Exception("Unexpected")
                
                index_id = self.getIndexID(index_type, trend_epoch)
                
                he = HistEvent(epoch, price, 
                     index_id, index_type, desc=data["bardiff"], 
                     data=data, color=color)
                hes.append(he)
                
                #if desc > 36:
                #    print(lib.epoch2dt(trend_epoch))
                
        return hes
    
        
    def _constructTrendlines(self, lastepoch, isTop=True):
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
                trendepochs[trend_epoch] = (trend_epoch, base_epoch, lastepoch)
                
        if isTop:
            self.top_trendlines = trendlines
            self.top_trendepochs = trendepochs
        else:
            self.bottom_trendlines = trendlines
            self.bottom_trendepochs = trendepochs
           
           
    def _updateMaxMin(self, lastepoch, isMax):
        exepoch,_,_,_,_,_ = self.subc.getBeforeNPrice(lastepoch, 
                                            self.minmax_keep_span)
        peak_exepoch,_,_,_,_,_ = self.subc.getBeforeNPrice(lastepoch, 
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
                (ep, top, _) = self.getMax()
                self.maxs[ep] = top
            else:
                (ep, bt, _) = self.getMin()
                self.mins[ep] = bt
            

            
def run(startep, endep, 
        instrument="USD_JPY", granularity="M5",
        peakspan=12*3, peaksize=5, analspan=12*4):
    from tools.subchart import SubChart
    from event.tick import TickEvent
    subc = SubChart("TrendlineIndex",
                                 instrument, 
                                 granularity,
                                 startep=startep,
                                 endep=endep,
                                 nbars=peakspan+peaksize*2,
                                 truncateOld=False)
    p = TrendLinesIndex(subc,peaksize, peakspan, analspan, deleteOld=False)
    tickEvent = TickEvent(endep,0,0,0)
    subc.onTick(tickEvent)
    p.onTick(tickEvent)
    return p.getPlotElements()      


if __name__ == "__main__":
    import env
    env.run_mode = env.MODE_BACKTESTING
    instrument = "USD_JPY"
    granularity = "M5"
    startep = lib.str2epoch("2019-11-28T00:00:00")
    endep = lib.str2epoch("2019-11-29T22:00:00")
        
    pes = run(startep, endep)
    #print(pes)
    
    import plotly.offline
    plotly.offline.init_notebook_mode()
    import lib.charts as m
    m.plot(instrument, granularity, 
           startep, endep, pes,datetime_display_span="h")
    
        
