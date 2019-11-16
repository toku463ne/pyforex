'''
Created on 2019/11/09

@author: kot
'''

from index import TechnicalIndex
from tools.subchart import SubChart

class PowerIndex(TechnicalIndex):
    


    def __init__(self, instrument, granularity, startep, endep, sumspan=20):
        super(PowerIndex, self).__init__(instrument, granularity)
        self.subc = SubChart("PowerIndex", instrument, granularity, startep, endep)
        self.sumspan = sumspan
        self.bull = []
        self.bear = []
        self.bull_totals = []
        self.bear_totals = []
        self.epochs = []
        (tl, _, hl, ll, cl, _) = self.subc.getPrices()
        self._calcPower(tl, hl, ll, cl)
        
    def _calcPower(self, tl, hl, ll, cl):
        bull = []
        bear = []
        for i in range(1, len(tl)):
            j = i-1
            u = hl[i]-ll[i]
            e = u
            c1 = cl[j]
            c2 = cl[i]
            
            d = c2 - c1
            if d >= 0:
                e -= d
                if e < 0:
                    e = 0
            else:
                u += d
                if u < 0:
                    u = 0
            bull.append(u)
            bear.append(e)
        
        for i in range(self.sumspan, len(bull)):
            self.bull_totals.append(sum(bull[i-self.sumspan:i]))
            self.bear_totals.append(sum(bear[i-self.sumspan:i]))
        
        self.bull.extend(bull[self.sumspan:])
        self.bear.extend(bear[self.sumspan:])
        self.epochs.extend(tl[self.sumspan+1:])
    