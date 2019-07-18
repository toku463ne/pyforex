'''
Created on 2019/05/01

@author: kot
'''
import env
from strategy import Strategy
from index.peaks import PeaksIndex
import lib.tradelib as tradelib
import lib

class PeakTriggerStrategy(Strategy):
    
    def __init__(self, instrument, granularity, startep, endep, 
                 cachesize=5, maxoldbars=10, profitpips=3, truncateOld=True):
        self.instrument = instrument
        self.id = -1
        self.peak5 = PeaksIndex(instrument, granularity, startep, endep, 12*24, 
                 5, cachesize, collect_last_changes=True)
        self.peak3 = PeaksIndex(instrument, granularity, startep, endep, 20*3, 
                 3, cachesize, collect_last_changes=True)
        self.pipprice = tradelib.pip2Price(1, instrument)
        self.profit = tradelib.pip2Price(profitpips, instrument)
        self.cnt = 0
        self.maxoldbars = maxoldbars
        self.nbars = 12*24
        self.truncateOld = truncateOld
        
        
        
    def onTick(self, tickEvent):
        epoch = tickEvent.time
        if self.id != -1:
            return
        
        (_id, t) = self.peak5.onTick(tickEvent)
        if self.truncateOld and _id > 0:
            if self.cnt >= self.maxoldbars:
                lib.printInfo(epoch, "Truncating old data")
                self.peak3.truncateOldFrom(_id-self.nbars)
                self.peak5.truncateOldFrom(_id-self.nbars)
                self.cnt = 0
            self.cnt += 1
            
        
        self.peak3.onTick(tickEvent)
        
        (_,o,h,l,c,_) = self.peak5.getPricesAt(_id-5,_id)
        if len(o) == 0:
            return
        
        
        valid_peaks = 0
        for _, hist in self.peak5.getLastChanged():
            valid_peaks += 1
            peak_price = hist.price
        if valid_peaks > 0:
            for _, hist in self.peak3.getLastChanged():
                if len(hist) >= 3:
                    valid_peaks += 1
        else:
            return
        
        if o[-1] < c[-1] and tickEvent.c > peak_price and tickEvent.c > c[-1]:
            side = env.SIDE_BUY
        elif o[-1] > c[-1] and tickEvent.c < peak_price and tickEvent.c < c[-1]:
            side = env.SIDE_SELL
        else:
            return
        
        
        self.peak5.clearLastChanges()
        self.peak3.clearLastChanges()
        
        
        if side == env.SIDE_BUY:
            price = tickEvent.ask
        else:
            price = tickEvent.bid
            
        if valid_peaks >= 3:
            pricediff = abs(max(h)-min(l)) - self.pipprice
            print(pricediff)
            if pricediff < self.profit:
                return
            
            desc = "peak=%.3f" % peak_price
            lib.printInfo(tickEvent.time, "orderC reason:%s" % desc)
            self.id = self.createOrder(tickEvent.time, self.instrument, side, 
                     env.ORDER_MARKET, 1, price, 
                     takeprofit_price=price+side*pricediff,
                     stoploss_price=price-side*pricediff,
                     desc=desc)
            
    def onSignal(self, signalEvent):
        if self.id == signalEvent.id:
            if signalEvent.signal >= env.ESIGNAL_TRADE_CLOSED:
                self.id = -1
        
    def getPlotElements(self, color="k"):
        ps = self.peak5.getPlotElement(color) 
        #ps.extend(self.peak5.getPlotElement(color)) 
        return ps
    
    
        