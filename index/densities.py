'''
Created on 2019/04/29

@author: kot
'''
from index import TechnicalIndex
from tools.subchart import SubChart
import lib.tradelib as tradelib
import lib
from plotelement.events import PlotEleEvents
#from tools.indexeddict import IndexedDict
from collections import OrderedDict
from event.info import InfoEvent
import env

class DensityIndex(TechnicalIndex):
    class Block():
        def __init__(self, epoch, density, std, mean):
            self.epoch = epoch
            self.density = density
            self.std = std
            self.mean = mean
            
            
    def __init__(self, instrument, granularity, startep, endep=-1, 
                 anal_span=5):
        super(DensityIndex, self).__init__(instrument, granularity)
        self.subc = SubChart(instrument, granularity, startep, 
                             endep, anal_span)
        self.now = -1
        self.anal_span = anal_span
        self.pipsize = tradelib.pip2Price(1, instrument)
        self.decimalPlace = tradelib.getDecimalPlace(instrument)
        #self.densdata = IndexedDict("densdata")
        self.densdata = OrderedDict()
        self.updateDens(startep)
        

        
    def onTick(self, tickEvent):
        i, epoch = self.subc.onTick(tickEvent)
        if i == -1 or epoch == self.now :
            return 
        
        if env.run_mode not in [env.MODE_BACKTESTING, env.MODE_UNITTEST]:
            self.updateDens(self.now+self.unitsecs)
            
            
        if epoch in self.densdata.keys():
            block = self.densdata[epoch]
            self.latestPriceList.upsert(epoch, block.mean, block)
            
        self.now = epoch
        


    def getCandle(self, epoch):
        i, _ = self.subc.getTime(epoch)
        j = self.nowidx - i
        (tl, ol, hl, ll, cl, vl) = self.subc.getPrices()
        return (tl[j],ol[j],hl[j],ll[j],cl[j],vl[j])
    

    def updateDens(self, startep=-1):
        if startep == -1:
            starti = -1
        else:
            starti, _ = self.subc.getTime(startep)
        
        anal_span = self.anal_span
        (tl, _, hl, ll, cl, _) = self.subc.getPrices()
        for i in range(starti, len(tl)):
            hl_c_rate,c_mean,hl_std = tradelib.getDensity(hl[i-anal_span+1:i+1], 
                                                    ll[i-anal_span+1:i+1], 
                                                    cl[i-anal_span+1:i+1])
            c_mean = lib.truncFromDecimalPlace(c_mean, self.decimalPlace)
            #self.densdata.append(tl[i], self.Block(tl[i],hl_c_rate,hl_std, c_mean))
            self.densdata[tl[i]] = self.Block(tl[i],hl_c_rate,hl_std, c_mean)
        
        if env.run_mode not in [env.MODE_BACKTESTING, env.MODE_UNITTEST]:
            t = tl[0]
            for k in list(self.densdata.keys()):
                if k >= t:
                    break
                del self.densdata[k]
        
        
    def data(self):
        return self.densdata
    
    def getPlotElement(self, color="k"):
        infoevents = []
        for ep in self.densdata.keys():
            block = self.densdata[ep]
            if block.density >= 0.8:
                infoevents.append(InfoEvent(ep , block.mean,
                                "density:\n %.3f" % block.density,
                                color=color))
        return PlotEleEvents(infoevents)
    
    
    def printDens(self):
        for ep in self.densdata.keys():
            b = self.densdata[ep]
            print("%s dens=%.3f mean=%.3f std=%.3f" % (lib.epoch2str(ep),
                b.density, b.mean, b.std))
    
    
    def sumNearest(self, price, rangeSize=0):
        cnt = 0
        max_edge = 0
        min_edge = 0
        for i in range(-rangeSize, rangeSize+1):
            obj, c = self.latestPriceList.searchObj(price+i*self.pipsize)
            if obj != None:
                ma = obj.std + obj.mean
                mi = obj.mean - obj.std
                if ma > max_edge:
                    max_edge = ma
                if mi == 0 or mi < min_edge:
                    min_edge = mi
                cnt += c
        return (cnt, min_edge, max_edge)
            