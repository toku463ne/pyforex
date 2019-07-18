'''
Created on 2019/05/20

@author: kot
'''
DIFF_SIZE = 0.1
import lib
DR_UP = 1
DR_DW = -1
DR_NO = 0

import matplotlib.pyplot as plt
import mpl_finance


class CandleShape(object):
    def __init__(self, unit_size=0.2):
        self.unit_size = unit_size
        patterns = lib.getRateList(int(1/unit_size), 3)
        patdict = {}
        
        i = 0
        for dr in [DR_UP, DR_DW, DR_NO]:
            for pat in patterns:
                patdict[(dr,)+pat] = i
                i += 1
        self.patdict = patdict
        rpatdict = {}
        for k in patdict.keys():
            rpatdict[patdict[k]] = k
        self.rpatdict = rpatdict
        
        
    
    def classify(self, o,h,l,c):
        size = h - l
        if size == 0:
            return ((-1,-1,-1,-1),-1)
        uhige = (h-max(o,c))/size
        dhige = (min(o,c)-l)/size
        jittai = abs(c-o)
        #d = jittai/(1/self.unit_size)
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
        
        shape = (dr, dhige, jittai2, uhige)
        n = self.patdict[shape]
        return (shape, n)
        
        
    def plot(self):
        nrows = len(self.patdict)
        
        o = []
        c = []
        for pat in self.patdict.keys():
            o.append(pat[0])
            c.append((pat[1] + pat[0]))
        
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        mpl_finance.candlestick2_ohlc(ax, opens=o, closes=c,lows=[0]*nrows, 
                                      highs=[1/self.unit_size]*nrows,
                          width=0.8, colorup='lightgray', colordown='grey', alpha=1)
    
    
if __name__ == "__main__":
    cs = CandleShape()
    
        
        
        
       
        