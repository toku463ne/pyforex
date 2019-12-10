'''
Created on 2019/12/09

@author: kot
'''
from index import TechnicalIndex
import const_candles
import lib
from tools.multiobjhistory import MultiObjHistory

class HistIndex(TechnicalIndex):
    def __init__(self, name, subChart, histSize=0):
        super(HistIndex, self).__init__(name, subChart)
        self.hist = MultiObjHistory()
        self.histSize = histSize
    
    def calcHistBasePrices(self, epoch):
        '''
        For example, price values on trend lines
        Returns list of event.history.HistEvent
        '''
        return []
    
    
    def calcHist(self, epoch):
        histEvents = self.calcHistBasePrices(epoch)
        if histEvents == None or len(histEvents) == 0:
            return
        
        i, epoch = self.subc.getTime(epoch)
        _,o,h,l,c,_ = self.subc.getPrice(i)
        candlelen = h-l
        if self.histSize > 0:
            expiration,_,_,_,_,_ = self.subc.getPrice(self.histSize) 
        else:
            expiration = 0
        for histEvent in histEvents:
            baseprice = histEvent.price
            
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
                print((lib.epoch2dt(epoch),o,h,l,c))
                raise Exception("Unexpected pattern")
            
            if epoch > 0 and abs(pos) <= const_candles.LINEDIST_BELOW_NEAR:
                histEvent.setPos(pos)
                self.hist.append(epoch, histEvent, expiration)
                histEvent.log(epoch)
                
    def getPlotElements(self, color="k"):
        from plotelement.hist import PlotEleHist
        pe = PlotEleHist(self.hist)
        return [pe]
        
        
                