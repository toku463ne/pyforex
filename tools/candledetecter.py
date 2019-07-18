'''
Created on 2019/05/27
@author: kot
'''
from tools.candleshape import CandleShape

class CandleDetecter(object):


    def __init__(self, tl,ol,hl,ll,cl,vl,unit_size=0.2):
        self.candles = (tl,ol,hl,ll,cl,vl)
        self.candleshape = CandleShape()
        self.unit_size = unit_size
        
        
    def isTonkachi(self, i, min_hige_rate=0.4):
        ret = (False, 0)
        min_hige_size = int(1/self.unit_size*min_hige_rate)
        (tl,ol,hl,ll,cl,vl) = self.candles
        t1 = tl[i-2]
        o1 = ol[i-2]
        h1 = hl[i-2]
        l1 = ll[i-2]
        c1 = cl[i-2]
        v1 = vl[i-2]
        t2 = tl[i-1]
        o2 = ol[i-1]
        h2 = hl[i-1]
        l2 = ll[i-1]
        c2 = cl[i-1]
        v2 = vl[i-1]
        t3 = tl[i]
        o3 = ol[i]
        h3 = hl[i]
        l3 = ll[i]
        c3 = cl[i]
        v3 = vl[i]
        
        ((dr,dhige, jittai, uhige), _) = self.cs.classify(o2, h2, l2, c2)
        if jittai <= 1:
            return ret
        
        pos = 0
        if uhige > dhige:
            if uhige > dhige:
                return ret
            if dhige < min_hige_size:
                return ret
            if o2 < c2:
                if o3 < c3:
                    return ret
            if max(c3,o3) >= max(o2,c2):
                return ret
            if min(c1,o1) < min(o2,c2):
                return ret
            if h1 >= h2:
                return ret
            pos = 1
        elif uhige < dhige:
            if uhige < dhige:
                return ret
            if jittai > min_hige_size:
                return ret
            if o2 > c2:
                if o3 > c3:
                    return ret
            if min(c1,o1) < min(o2,c2):
                return ret
            if max(c3,o3) < max(o2,c2):
                return ret
            if l1 <= l2:
                return ret
            pos = -1
        else:
            return ret
        
        return (True, pos)
        