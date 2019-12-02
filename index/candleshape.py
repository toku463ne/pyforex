'''
Created on 2019/11/24

@author: kot
'''
import const_candles

DIFF_SIZE = 0.1
DR_UP = 1
DR_DW = -1
DR_NO = 0

from index import TechnicalIndex
import lib
import numpy as np

class CandleShapeIndex(TechnicalIndex):

    def __init__(self, subChart, 
                 unit_size=0.2,
                 statistics_span=6*12):
        super(CandleShapeIndex, self).__init__("CandleShapeIndex", 
                                        subChart.instrument, 
                                        subChart.granularity)
        self.statistics_span = statistics_span
        self.subc = subChart
        self.unit_size = unit_size
        patterns = lib.getRateList(int(1/unit_size), 3)
        patdict = {}
        
        i = 0
        for pat in patterns:
            patdict[pat] = i
            i += 1
        self.patdict = patdict
        rpatdict = {}
        for k in patdict.keys():
            rpatdict[patdict[k]] = k
        self.rpatdict = rpatdict
        
        self.candle_len_avg = 0
        self.candle_len_std = 0
        
        
        
    def classify(self, o,h,l,c):
        size = h - l
        if size == 0:
            return (0, (-1,-1,-1),-1)
        uhige = (h-max(o,c))/size
        dhige = (min(o,c)-l)/size
        d = 0
        is_up = (c-o-d > 0)
        is_down = (c-o+d < 0)
        
        dr = DR_NO
        if is_up:
            dr = DR_UP
        elif is_down:
            dr = DR_DW
            
        us = int(1/self.unit_size)
        uhige = int(us*uhige)
        dhige = int(us*dhige)
        jittai2 = us - (uhige+dhige)
        
        shape = (dhige, jittai2, uhige)
        n = self.patdict[shape]
        return (dr, shape, n)
    
    def classifypair(self, o1,h1,l1,c1,
                     o2,h2,l2,c2):
        attrs = []
        # harami
        if (h1 > h2 and l1 <= l2) or (h1 >= h2 and l1 < l2):
            attrs.append(const_candles.CANDLEPAIR_HARAMI)
        if (h1 < h2 and l1 >= l2) or (h1 <= h2 and l1 > l2):
            attrs.append(const_candles.CANDLEPAIR_FUKUMI)
        if h1 < h2 and l1 < l2:
            attrs.append(const_candles.CANDLEPAIR_UPDOW)
        if h1 > h2 and l1 > l2:
            attrs.append(const_candles.CANDLEPAIR_DOWNDOW)
        if h1 < l2 or l1 > h2:
            attrs.append(const_candles.CANDLEPAIR_GAP)
            
        return attrs
            
    
    def onTick(self, tickEvent):
        epoch = tickEvent.time
        i, epoch = self.subc.getTime(epoch)
        if epoch == self.now:
            return None

        self.now = epoch
        
        candlelen_avg = 0
        candlelen_std = 0
        vol_avg = 0
        vol_std = 0
        
        
        (_,ol,hl,ll,cl,vl) = self.subc.getPrices()
        if i >= self.statistics_span-1:
            hn = np.array(hl[i-self.statistics_span:i+1])
            ln = np.array(ll[i-self.statistics_span:i+1])
            vn = np.array(vl[i-self.statistics_span:i+1])
            dn = hn - ln
            candlelen_avg = dn.mean()
            candlelen_std = dn.std()
            vol_avg = vn.mean()
            vol_std = vn.std()
        
        (dr, shape, _id) = self.classify(ol[i], hl[i], ll[i], cl[i])
        j = i-1
        pairattrs = self.classifypair(ol[j], hl[j], ll[j], cl[j], 
                                      ol[i], hl[i], ll[i], cl[i])
        
        return (dr, shape, _id, 
                (candlelen_avg, candlelen_std), 
                (vol_avg, vol_std), pairattrs)