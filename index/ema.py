'''
Created on 2019/04/14

@author: kot
'''
from index import TechnicalIndex
from tools.subchart import SubChart


class EmaIndex(TechnicalIndex):
    
    def __init__(self, instrument, granularity, startep, endep, ema_span=5):
        super(EmaIndex, self).__init__(instrument, granularity)
        self.subc = SubChart(instrument, granularity, startep, 
                             endep)
        (t, _, _, _, cl, _) = self.subc.getPrices()
        self.epochs = t[ema_span:]
        self.alpha = 2.0/(ema_span+1)
        self.ema_span = ema_span
        self.now = 0
        
        first_ema = sum(cl[:ema_span]) / ema_span
        self.ema = []
        self._calcEma(t[ema_span-1:], cl[ema_span-1:], first_ema)
        
        
    def _calcEma(self, t, cl, last_ema):
        ema = self.ema
        for i in range(1,len(cl)):
            if t[i]-t[i-1]>self.unitsecs:
                preema = cl[i]
            else:
                preema = last_ema
            last_ema = preema + self.alpha*(cl[i]-preema)
            ema.append(last_ema)
            
        self.ema = ema
        
        
    def onTick(self, tickEvent):
        epoch = tickEvent.time
        i, epoch = self.subc.getTime(epoch)
        if epoch == self.now:
            return i, epoch, self.ema[i]
        
        if i < 0:
            self.updateEma()
        
        self.now = epoch
    
        mprice = (tickEvent.bid + tickEvent.ask)/2
        
        i = i - self.ema_span
        if i >= 0:
            return i, epoch, self.ema[i] 
        else:
            return i, epoch, -1
        
        
            
    def updateEma(self):
        (t1, _, _, _, cl1, _) = self.subc.getLatestChart(self.epochs[-1])
        self._calcEma(t1, cl1, self.ema[-1])
    
        
