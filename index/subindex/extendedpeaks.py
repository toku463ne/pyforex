'''
Created on 2019/12/08

@author: kot
'''
from index.subindex import SubIndex

class ExtendedPeaksIndex(SubIndex):
    
    def __init__(self, subc, minmax_keep_span=12*24):
        self.minmax_keep_span = minmax_keep_span
        self.subc = subc
        
    
    def calc(self, lastepoch, peakepoch, top_bottom_updated):
        exepoch,_,_,_,_,_ = self.subc.getBeforeNPrice(lastepoch, 
                                            self.minmax_keep_span)
        peak_exepoch,_,_,_,_,_ = self.subc.getBeforeNPrice(lastepoch, 
                                            self.peakspan)
        if top_bottom_updated == 1:
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
            if top_bottom_updated == 1:
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
            if top_bottom_updated == 1:
                (ep, top) = self.getMax()
                self.maxs[ep] = top
            else:
                (ep, bt) = self.getMin()
                self.mins[ep] = bt
        
    def getPlotElements(self, color="k"):
        pass
        