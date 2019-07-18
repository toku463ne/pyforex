'''
Created on 2019/04/14

@author: kot
'''

from strategy import Strategy
import lib
import lib.tradelib as tradelib
from index.ema import EmaIndex
from index.peaks import PeaksIndex
from index.densities import DensityIndex
from index.std import StdIndex
from index.std import STD_TYPE_CANDLE_LEN
import env

class SlopeStrategy(Strategy):
    
    def __init__(self, instrument, granularity, startep, 
                 endep=-1, ema_span=20, profitpips=5,
                 cachesize=5,
                 peak_span=6,
                 parent_peak_span=3,
                 parent_granularity="D",
                 dens_anal_span=5,
                 maxoldbars=12*24,truncateOld=True):
        self.lastep = 0
        self.instrument = instrument
        self.granularity = granularity
        self.unitsecs = tradelib.getUnitSecs(granularity)
        if endep == -1:
            endep = lib.nowepoch()
        
        self.decimalPlace = tradelib.getDecimalPlace(instrument)
        self.ema = EmaIndex(instrument, granularity, startep, endep, ema_span)
        self.peak = PeaksIndex(instrument, granularity, startep, endep, maxoldbars, 
                 peak_span, cachesize, collect_last_changes=True)
        self.parent_peak = PeaksIndex(instrument, parent_granularity, 
                startep, endep, maxoldbars, parent_peak_span, 
                cachesize, collect_last_changes=True)
        self.dens = DensityIndex(instrument, granularity, 
                startep, endep=endep, 
                anal_span=dens_anal_span)
        #self.std = StdIndex(instrument, granularity, startep, 
        #                    endep, ema_span, std_type=STD_TYPE_CANDLE_LEN)
        self.profit = tradelib.pip2Price(profitpips, instrument)
        
        self.trancateOld=truncateOld
        self.id = -1
        self.den_l = -1
        self.den_u = -1
        self.onTrade = False
        
    
    
    def onTick(self, tickEvent):
        #if tickEvent.time >= lib.str2epoch("2019-04-04T12:00:00", 
        #                                  "%Y-%m-%dT%H:%M:%S"):
        #    print(lib.epoch2dt(tickEvent.time))
        
        h = tickEvent.h
        l = tickEvent.l
        c = tickEvent.c
        price = (h+l+c)/3
        
        if not self.peak.onTick(tickEvent):
            return
        self.parent_peak.onTick(tickEvent)
        self.dens.onTick(tickEvent)
        #self.std.onTick(tickEvent)
        #curstd = self.std.get()
        #if curstd*2 < self.profit:
        #    return
        
        
        direction = 0
        curstd = 0
        pobj = None
        cnt = 0
        (den_l, den_u) = self.dens.searchNearest(price)
        if den_l > 0 and den_u == -1:
            pobj,cnt = self.dens.searchObj(den_l)
            if price > den_l + pobj.std:
                curstd = pobj.std
                direction = 1
        elif den_u > 0 and den_l == -1:
            pobj,cnt = self.dens.searchObj(den_u)
            if price < den_u - pobj.std:
                curstd = pobj.std
                direction = -1
        elif den_u > 0 and den_l > 0:
            den_m = (den_u + den_l)/2
            if price > den_m:
                pobj,cnt = self.dens.searchObj(den_u)
                if price < den_u - pobj.std:
                    curstd = pobj.std
                    direction = -1
            elif price < den_m:
                pobj,cnt = self.dens.searchObj(den_l)
                if price > den_l + pobj.std:
                    curstd = pobj.std
                    direction = 1
        
        if direction == 0:
            return
        
        if cnt < 3:
            return
        
        if den_l == self.den_l and den_u == self.den_u and self.onTrade:
            return
            
        (_,o,h,l,c,_) = self.dens.getCandle()
        if (c-o)*direction <= 0:
            return
        
        pricediff = h-l
        if pricediff < 2*curstd:
            return
        
        #(peak_l, peak_u) = self.peak.searchNearest(price)
        #(ppeak_l, ppeak_u) = self.parent_peak.searchNearest(price)
        
        '''
        side = 0
        if direction == 1:
            if (peak_u == -1 or \
                 price < peak_u-curstd/2 and price < ppeak_u-curstd/2):
                side = env.SIDE_BUY
        if direction == -1:
            if (peak_l == -1 or \
                 price > peak_l+curstd/2 and price > ppeak_l+curstd/2):
                side = env.SIDE_SELL
        
        if side == 0:
            return
        '''
        side = direction
        #pricediff = curstd
        
        lib.printInfo(tickEvent.time, "orderC price:%.3f" % price)
        self.id = self.createOrder(tickEvent.time, 
                self.instrument, side, 
                 env.ORDER_MARKET, 1, price, 
                 takeprofit_price=price+side*pricediff,
                 stoploss_price=price-side*pricediff,
                 ) 

        
    def getPlotElements(self, color="k"):
        ps = []
        p = self.peak.getPlotElement(color) 
        ps.extend(p)
        p = self.parent_peak.getPlotElement(color) 
        ps.extend(p)
        p = self.dens.getPlotElement(color)
        ps.append(p)
        return ps
    
    
    
    