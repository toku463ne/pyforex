'''
Created on 2019/12/08

@author: kot
'''

from index.subindex import SubIndex
import const_candles
import lib
from tools.history import History


class HistEvent(object):
    def __init__(self, price, line_type, pos):
        self.price = price
        self.line_type = line_type
        self.pos = pos
        
    def log(self, ep):
        lt = ""
        line_type = self.line_type
        if line_type == const_candles.LINE_TPTREND:
            lt = "tp"
        elif line_type == const_candles.LINE_BTTREND:
            lt = "bt"
        elif line_type == const_candles.LINE_MAX:
            lt = "ma"
        elif line_type == const_candles.LINE_MIN:
            lt = "mi"
        ps = ""
        pos = self.pos
        if pos == const_candles.LINEDIST_ABOVE_FAR:
            ps = "ab_far"
        elif pos == const_candles.LINEDIST_ABOVE_NEAR:
            ps = "ab_nea"
        elif pos == const_candles.LINEDIST_ABOVE_TOUCHED:
            ps = "ab_tou"
        elif pos == const_candles.LINEDIST_CROSSED:
            ps = "cross"
        elif pos == const_candles.LINEDIST_BELOW_FAR:
            ps = "bl_far"
        elif pos == const_candles.LINEDIST_BELOW_NEAR:
            ps = "bl_nea"
        elif pos == const_candles.LINEDIST_BELOW_TOUCHED:
            ps = "bl_tou"
        lib.printDebug(ep, "id=%s type=%s pos=%s" % (
            self.line_id, lt, ps))
        

class LineTouchIndex(SubIndex):

    def __init__(self, subChart, size, deleteOld=True):
        self.size = size
        self.hist = History(size, deleteOld)
        super(LineTouchIndex, self).__init__(subChart)
        
    def calcLinePrices(self, epoch):
        pass
    
    def calc(self, epoch, line_type):
        baseprice = self.calcLinePrice(epoch)
        
        i, epoch = self.subc.getTime(epoch)
        _,o,h,l,c,_ = self.subc.getPrice(i)
    
        candlelen = h-l
        pos = 0
        if h < baseprice - candlelen*0.2:
            pos = const_candles.LINEDIST_ABOVE_FAR
        elif h < baseprice:
            pos = const_candles.LINEDIST_ABOVE_NEAR
        elif h >= baseprice and max(o,c) <= baseprice:
            pos = const_candles.LINEDIST_ABOVE_TOUCHED
        elif max(o,c) >= baseprice and min(o,c) <= baseprice:
            pos = const_candles.LINEDIST_CROSSED
        elif min(o,c) >= baseprice and l <= baseprice:
            pos = const_candles.LINEDIST_BELOW_TOUCHED
        elif l - candlelen*0.2 < baseprice:
            pos = const_candles.LINEDIST_BELOW_NEAR
        elif l > baseprice:
            pos = const_candles.LINEDIST_BELOW_FAR
        else:
            raise Exception("Unexpected pattern")
        
        if epoch > 0 and abs(pos) <= const_candles.LINEDIST_BELOW_NEAR:
            he = HistEvent(baseprice, line_type, pos)
            self.hist.append(epoch, he)
            he.log(epoch)
        
    def getPlotElements(self, color="k"):
        from plotelement.minievents import PlotEleMiniEvents
        from event.info import InfoEvent
        
        ies = []
        for (epoch, hes) in list(self.hist.history.items()):
            for he in hes:
                if he.line_type == const_candles.LINE_TPTREND:
                    marker="x"
                    color="r"
                elif he.line_type == const_candles.LINE_BTTREND:
                    marker="x"
                    color="b"
                elif he.line_type == const_candles.LINE_MAX:
                    marker="_"
                    color="r"
                elif he.line_type == const_candles.LINE_MIN:
                    marker="_"
                    color="b"
                else:
                    marker="x"
                    color="black"
                    
                ies.append(InfoEvent(epoch, he.price, "", 
                                     marker=marker,color=color))
            
        return [PlotEleMiniEvents(ies)]
        
        