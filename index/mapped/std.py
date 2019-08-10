'''
Created on 2019/08/03

@author: kot
'''

from index.mapped import MappedIndex
import lib
from plotelement.linechart import PlotEleLineChart
import numpy as np


class STDMappedIndex(MappedIndex):
    class Block():
        def __init__(self, price, std):
            self.price = price
            self.std = std
    
    def __init__(self, instrument, granularity, startep, endep=-1, 
                 anal_span=5, maxsize=12*24*3, map_cache_len=12*24):
        super(STDMappedIndex, self).__init__(instrument, 
                                            granularity, 
                                            startep, endep, 
                                            anal_span, maxsize, map_cache_len)
    
    def __str__(self):
        out = ""
        for ep in self.data.keys():
            m,s = self.data[ep]
            out = "%s%s mean=%.3f std=%.3f\n" % (out, lib.epoch2str(ep),m,s)
        return out
        
    # return map_key, map_val 
    def calcData(self, subcIdx):
        n = self.anal_span
        errret = (-1,-1)
        if subcIdx-self.anal_span < 0:
            return errret
        (_, _, h, l, c, _) = self.subc.getPrices(subcIdx-self.anal_span+1,
                                                 subcIdx)
        if len(h) < n:
            return errret
        a = h+l+c
        price = np.mean(a)
        pstd = np.std(a)
        map_key = lib.truncFromDecimalPlace(price, self.decimalPlace)
        map_val = pstd
        return (map_key, map_val)
        
    def sumNearest(self, price, rangeSize=0):
        cnt = 0
        max_edge = 0
        min_edge = 0
        for i in range(-rangeSize, rangeSize+1):
            s, c = self.latestPriceList.searchObj(price+i*self.pipsize)
            if c > 0:
                ma = s + price
                mi = price - s
                if ma > max_edge:
                    max_edge = ma
                if min_edge == 0 or mi < min_edge:
                    min_edge = mi
                cnt += c
        return (cnt, min_edge, max_edge)
    
    
    
    def getPlotElements(self, color="k"):
        sma = []
        smau = []
        smad = []
        epochs = []
        for t in self.data.keys():
            (me, st) = self.data[t]
            if me == -1:
                continue
            sma.append(me)
            smau.append(me+st)
            smad.append(me-st)
            epochs.append(t)
            
        p1 = PlotEleLineChart(epochs, sma, color=color)
        p2 = PlotEleLineChart(epochs, smau, color=color)
        p3 = PlotEleLineChart(epochs, smad, color=color)
        return [p1,p2,p3]
        
    