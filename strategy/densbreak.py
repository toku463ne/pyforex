'''
Created on 2019/04/14

@author: kot
'''

from strategy import Strategy
import lib
import lib.tradelib as tradelib
from index.mapped.std import STDMappedIndex
from index.checker import CheckIndex
import env

CNT_OPEN_WINDOW = 3
CNT_VALID_DENS = 3
DENSE_SIZE_PIPS = 3
NON_TRADE_HOUR_ST = 11
NON_TRADE_HOUR_ED = 14


class DensBreakStrategy(Strategy):
    
    def __init__(self, instrument, startep, 
                 endep=-1, min_profitpips=5, max_profitpips=15,
                 anal_span=5, granularity="H1"):
        self.instrument = instrument
        self.granularity = granularity
        self.unitsecs = tradelib.getUnitSecs(granularity)
        if endep == -1:
            endep = lib.nowepoch()
        
        self.decimalPlace = tradelib.getDecimalPlace(instrument)
        self.checker = CheckIndex(instrument, granularity, startep, endep)
        self.stdmap = STDMappedIndex(instrument, granularity, 
                                     startep, endep,
                                     anal_span=anal_span)

        self.min_profit = tradelib.pip2Price(min_profitpips, instrument)
        self.max_profit = tradelib.pip2Price(max_profitpips, instrument)
        self.bid_id = -1
        self.ask_id = -1
        self.den_l = -1
        self.den_u = -1
        self.lastDensTraded = -1
        self.lastSide = 0
        
    
    
    def onTick(self, tickEvent):
        h = tickEvent.h
        l = tickEvent.l
        c = tickEvent.c
        price = (h+l+c)/3
        #if tickEvent.time >= lib.str2epoch("2017-01-27T21:00:00", 
        #                                  "%Y-%m-%dT%H:%M:%S") and price >= 111.50:
        #    lib.printDebug(tickEvent.time, price)
        
        if self.checker.onTick(tickEvent) == False:
            return
        if self.checker.isHourRange(NON_TRADE_HOUR_ST, NON_TRADE_HOUR_ED):
            return
        if not self.checker.isNHoursAfterWeekend(2):
            return
        if not self.checker.isNHoursBeforeWeekend(2):
            if self.ask_id >= 0:
                lib.printInfo(tickEvent.time, "Closing trade %d due to Friday night." % self.ask_id)
                self.closeTrade(self.ask_id)
            if self.bid_id >= 0:
                lib.printInfo(tickEvent.time, "Closing trade %d due to Friday night." % self.bid_id)
                self.closeTrade(self.bid_id)
            
            return
        if self.checker.isNextOK() == False:
            return 
        
        self.stdmap.onTick(tickEvent)
        
        
        direction = 0
        curstd = 0
        lastDensTraded = 0
        (den_l, den_u) = self.stdmap.searchNearest(price)
        if den_l > 0 and den_u == -1:
            direction = 1
            lastDensTraded = den_l
        elif den_u > 0 and den_l == -1:
            direction = -1
            lastDensTraded = den_u
        elif den_u > 0 and den_l > 0:
            den_m = (den_u + den_l)/2
            if price > den_m:
                direction = -1
                lastDensTraded = den_u
            else:
                direction = 1
                lastDensTraded = den_l
        else:
            return
        
        if self.ask_id >= 0 and direction == env.SIDE_BUY:
            return
        if self.bid_id >= 0 and direction == env.SIDE_SELL:
            return
        
        stdv,_ = self.stdmap.searchObj(lastDensTraded)
        if stdv >= 0 and price*direction > lastDensTraded + stdv*direction:
            curstd = stdv
            
        
                               
        if lastDensTraded == 0 or lastDensTraded == self.lastDensTraded:
            return

        
        if self.checker.isDowCandle(direction) == False:
            return
        
        
        if self.checker.isWindowOpen(curstd):
            self.checker.addForNext(CNT_OPEN_WINDOW)
            return
        
            
        (_,o,h,l,c,_) = self.checker.getPriceAt()
        if (c-o)*direction <= 0:
            return
        
        pricediff = h-l
        if pricediff < 2*curstd:
            return
        
        if pricediff < self.min_profit:
            return
        
        if pricediff > self.max_profit:
            pricediff = self.max_profit
        
        (cnt, ma, mi) = self.stdmap.sumNearest(lastDensTraded, DENSE_SIZE_PIPS)
        if cnt < CNT_VALID_DENS:
            return
        
        if direction > 0 and price < ma:
            return
        if direction < 0 and price > mi:
            return
        
        
        
        side = direction
        
        lib.printInfo(tickEvent.time, "orderC price:%.3f" % price)
        _id = self.createOrder(tickEvent.time, 
                self.instrument, side, 
                 env.ORDER_MARKET, 1, price, 
                 takeprofit_price=price+side*pricediff,
                 stoploss_price=price-side*pricediff,
                 ) 
        if side == env.SIDE_BUY:
            self.ask_id = _id
        if side == env.SIDE_SELL:
            self.bid_id = _id
        self.lastDensTraded = lastDensTraded*direction
        self.lastSide = side

        
    def getPlotElements(self, color="k"):
        ps = []
        p = self.stdmap.getPlotElement(color)
        ps.append(p)
        return ps
    
    
    def onSignal(self, signalEvent):
        if signalEvent.signal >= env.ESIGNAL_TRADE_CLOSED:
            if signalEvent.trade_event.side == env.SIDE_BUY:
                self.ask_id = -1
            if signalEvent.trade_event.side == env.SIDE_SELL:
                self.bid_id = -1
            

    
    