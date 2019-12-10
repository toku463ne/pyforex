'''
Created on 2019/11/16

@author: kot
'''
from strategy import Strategy
import env
import lib.tradelib as tradelib
import lib
from tools.subchart import SubChart
from tools.multiobjhistory import MultiObjHistory
from tools.history import History
from index.peaks import PeakIndex
from index.candleshape import CandleShapeIndex
import const_candles

class HistEvent(object):
    def __init__(self, line_id, line_type, pos, coord):
        self.line_id = line_id
        self.line_type = line_type
        self.pos = pos
        self.coord = coord

        
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
        lib.printDebug(ep, "id=%s type=%s pos=%s coord=%.3f" % (
            self.line_id, lt, ps, self.coord))
        if line_type == const_candles.LINE_BTTREND:
            te = self.peaks.bottom_trendepochs
        elif line_type == const_candles.LINE_TPTREND:
            te = self.peaks.top_trendepochs
        if line_type in [const_candles.LINE_BTTREND, const_candles.LINE_TPTREND]:
            lib.printDebug(ep, "%s %s %s" % (te[0],te[1],te[2]))
        

class PriceActionStrategy(Strategy):
    def __init__(self, instrument, granularity, 
                 startep=-1, endep=-1,
                 peakspan = 12*6,
                 peaksize = 5,
                 analspan = 12*4
        ):
        
        self.instrument = instrument
        self.granularity = granularity
        self.subc = SubChart("PriceAction",
                                 self.instrument, 
                                 self.granularity,
                                 startep=startep,
                                 endep=endep,
                                 nbars=peakspan+peaksize*2)
        
        self.peaks = PeakIndex(self.subc, peaksize, peakspan)
        self.analspan = analspan
        self.hist = MultiObjHistory(analspan)
        self.candleshapes = CandleShapeIndex(self.subc,
                            statistics_span=analspan)
        self.unitsecs = tradelib.getUnitSecs(granularity)
        self.pipprice = tradelib.pip2Price(1, instrument)
        self.nowi = -1
        self.now = -1
        
        self.linehists = {
            const_candles.LINE_TPTREND: {}, # dict of History()
            const_candles.LINE_BTTREND: {},
            const_candles.LINE_MAX: {},
            const_candles.LINE_MIN: {}
            }
    
    def updateLineHistory(self, line_id, linehist, 
                          line_type, coord, epoch, pos):
        lastepoch, lastpos = linehist.last()
        if lastepoch > 0 and abs(lastpos) <= const_candles.LINEDIST_ABOVE_NEAR:
            he = HistEvent(line_id, line_type, pos, coord)
            self.hist.append(epoch, he)
            self.hist.log(epoch)
        linehist.append(epoch, pos)
        lib.printDebug(epoch, "id=%s type=%s pos=%s coord=%.3f" % (
            line_id, line_type, pos, coord))
    
    def getLineID(self, epoch, line_type):
        return "%d_%d" % (line_type, epoch)
    
    def detectLineDist(self):
        tprices = self.peaks.getPriceOnTrendlines(self.now, True)
        bprices = self.peaks.getPriceOnTrendlines(self.now, False)
        maxs = self.peaks.maxs.items()
        mins = self.peaks.mins.items()
        t,o,h,l,c,_ = self.subc.getPrice()
        candlelen = h-l
        expiration,_,_,_,_,_ = self.subc.getPrice(self.analspan) 
        for (baseps, ltype) in [
            (tprices, const_candles.LINE_TPTREND),
            (bprices, const_candles.LINE_BTTREND),
            (maxs, const_candles.LINE_MAX),
            (mins, const_candles.LINE_MIN)]:
            lines = self.linehists[ltype]
            
            for line_id in list(lines.keys()):
                (lastep, _) = lines[line_id].last()
                if lastep < expiration:
                    del lines[line_id]
            
            for items in baseps:
                if ltype in [const_candles.LINE_TPTREND,const_candles.LINE_BTTREND]:
                    line_epoch, baseprice, coord = items
                else:
                    line_epoch, baseprice = items
                    coord = baseprice
                line_id = self.getLineID(line_epoch, ltype)
                if line_id in lines.keys():
                    linehist = lines[line_id]
                else:
                    linehist = History(self.analspan)
                pos = 0
                if h < baseprice - candlelen*0.2:
                    pos = const_candles.LINEDIST_ABOVE_FAR
                elif h < baseprice:
                    pos = const_candles.LINEDIST_ABOVE_NEAR
                elif h >= baseprice and max(o,c) <= baseprice:
                    pos = const_candles.LINEDIST_ABOVE_TOUCHED
                elif max(o,c) > baseprice and min(o,c) < baseprice:
                    pos = const_candles.LINEDIST_CROSSED
                elif min(o,c) >= baseprice and l <= baseprice:
                    pos = const_candles.LINEDIST_BELOW_TOUCHED
                elif l - candlelen*0.2 < baseprice:
                    pos = const_candles.LINEDIST_BELOW_NEAR
                elif l > baseprice:
                    pos = const_candles.LINEDIST_BELOW_FAR
                #linehist.append(t, pos)
                self.updateLineHistory(line_id, linehist, 
                                       ltype, coord, t, pos)
            
    
    def onTick(self, tickEvent):        
        now = self.subc.onTick(tickEvent)
        if now == self.now:
            return []
        self.now = now
        
        self.candleshapes.onTick(tickEvent)
        self.peaks.onTick(tickEvent)
        
        self.detectLineDist()
        
        orders = []
        #if lib.str2epoch("2019-11-15T00:30:00") == tickEvent.time:
        #    print(tickEvent.time)
        '''
        if self.id == -1:
            self.curr_side *= -1
            if self.curr_side == env.SIDE_BUY:
                price = tickEvent.l - self.pipprice*3
            else:
                price = tickEvent.h + self.pipprice*3
        
            order = self.createStopOrder(
                    tickEvent, self.instrument, self.curr_side, 1, 
                    price,
                    validep=tickEvent.time+self.unitsecs,
                    takeprofit=price+self.curr_side*self.profit, 
                    stoploss=price-self.curr_side*self.profit)
            if order != None:
                self.id = order.id
                orders.append(order)
        '''
            
        return orders
        
        
    def onSignal(self, signalEvent):
        if self.id == signalEvent.id:
            if signalEvent.signal in [env.ESTATUS_ORDER_CLOSED,
                                      env.ESTATUS_TRADE_CLOSED]:
                self.id = -1
        