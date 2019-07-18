'''
Created on 2019/04/14

@author: kot
'''
from index import TechnicalIndex
from tools.subchart import SubChart

import numpy as np 
STD_TYPE_DEFAULT = 0
STD_TYPE_CANDLE_LEN = 1

class StdIndex(TechnicalIndex):
    
    def __init__(self, instrument, granularity, startep, endep, 
                 std_span=5, std_type=STD_TYPE_DEFAULT):
        super(StdIndex, self).__init__(instrument, granularity)
        self.subc = SubChart(instrument, granularity, startep, 
                             endep)
        self.std_type = std_type
        self.std = []
        (t, _, hl, ll, cl, _) = self.subc.getPrices()
        for i in range(std_span-1, len(t)):
            self._calcStd(hl[i-std_span+1:i+1], 
                      ll[i-std_span+1:i+1],
                      cl[i-std_span+1:i+1])
            
        self.epochs = t[std_span-1:]
        
        self.std_span = std_span
        self.now = 0
        self.nowidx = -1
        
        
        
    def _calcStd(self, hl, ll, cl):
        std = self.std
        if self.std_type == STD_TYPE_DEFAULT:
            std.append(np.std(hl+ll+cl))
        elif self.std_type == STD_TYPE_CANDLE_LEN:
            hn = np.array(hl)
            ln = np.array(ll)
            np.std(hn-ln)
        
        self.std = std
        
        
    def getCandle(self, i=0):
        j = self.nowidx - i
        (tl, ol, hl, ll, cl, vl) = self.subc.getPrices()
        return (tl[j],ol[j],hl[j],ll[j],cl[j],vl[j])
    
        
    def onTick(self, tickEvent):
        epoch = tickEvent.time
        i, epoch = self.subc.getTime(epoch)
        if epoch == self.now:
            return i, epoch, self.std[i]
        
        if i < 0:
            self.updateStd()
        
        self.now = epoch
        self.nowidx = i
    
        i = i - self.std_span
        if i >= 0:
            return i, epoch, self.std[i] 
        else:
            return i, epoch, -1
        
        
            
    def updateStd(self):
        (t, _, hl, ll, cl, _) = self.subc.getLatestChart(self.epochs[-1])
        i = self.nowidx + 1
        if i >= len(t):
            epoch = t[i]
            return
        std_span = self.std_span
        while epoch < t[-1]:
            self._calcStd(hl[i-std_span+1:i+1], 
                      ll[i-std_span+1:i+1],
                      cl[i-std_span+1:i+1])
            i += 1
            if i >= len(t):
                break
            epoch = t[i]
        self.now = i
    
    def get(self, i=0):
        return self.std[self.nowidx-i-self.std_span+1]

