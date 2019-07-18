'''
Created on 2019/04/14

@author: kot
'''
from index import TechnicalIndex
import lib.getter as getter

class SmaIndex(TechnicalIndex):
    
    def __init__(self, instrument, granularity, startep, endep, sma_span=5):
        super(SmaIndex, self).__init__(instrument, granularity)
        (t,_,_,_,cl,_) = getter.getPrices(instrument, granularity, startep, endep)
        self.time = t[sma_span-1:]
        
        tmpsum = sum(cl[:sma_span])
        sma = [0]*(len(t)-sma_span)
        sma[0] = tmpsum / sma_span
        j = 1
        for i in range(sma_span+1, len(cl)):
            tmpsum += cl[i]
            tmpsum -= cl[j]
            sma[j] = tmpsum / sma_span
            j += 1
        
        self.epochs = t[sma_span:]
        self.sma = sma
        
        
