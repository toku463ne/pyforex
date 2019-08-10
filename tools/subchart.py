'''
Created on 2019/05/01

@author: kot
'''
import lib
import lib.tradelib as tradelib
from collections import OrderedDict
import lib.getter as getterlib
import env
EP = 0
O = 1
H = 2
L = 3
C = 4
V = 5


class SubChart(object):
    def __init__(self, name, instrument, granularity, 
                 startep=-1, endep=-1, 
                 nbars=0, maxsize=12*24*3):
        self.name = name
        self.instrument = instrument
        self.granularity = granularity
        self.unitsecs = tradelib.getUnitSecs(granularity)
        self.epochsidx = None
        self.nowidx = -1
        self.now = -1
        self.maxsize = maxsize
        self.size_to_cleanup = int(maxsize*1.5)
        
        if startep == -1:
            startep = lib.nowepoch()
        if endep == -1:
            endep = lib.nowepoch()
        (t,o,h,l,c,v) = getterlib.getPrices(instrument, 
                                            granularity, startep, endep+1)
        if nbars > 0:
            (t1,o1,h1,l1,c1,v1) = getterlib.getNPrices(instrument, 
                                                       granularity, startep-1, nbars)
            t1.extend(t)
            o1.extend(o)
            h1.extend(h)
            l1.extend(l)
            c1.extend(c)
            v1.extend(v)
            (t,o,h,l,c,v) = (t1,o1,h1,l1,c1,v1)
        self.prices = (t,o,h,l,c,v)
        self._initCaches()
        self.startep = t[0]
        self.endep = t[-1]
        
        
    
    def _initCaches(self):
        self.epochsidx = OrderedDict()
        t = self.prices[EP]
        for i in range(len(t)):
            self.epochsidx[t[i]] = i
        
    # returns number of shift
    def truncateOldFrom(self):
        try:
            if env.run_mode in [env.MODE_BACKTESTING, env.MODE_UNITTEST]:
                return
            (t,o,h,l,c,v) = self.prices
            if self.nowidx+1 <= self.size_to_cleanup:
                return
            #starti = len(t[:self.nowidx+1]) - self.maxsize
            starti = self.nowidx+1-self.maxsize
            lib.printInfo(self.now, "%s subchart | truncating old chart" % self.name)
            t = t[starti:]
            o = o[starti:]
            h = h[starti:]
            l = l[starti:]
            c = c[starti:]
            v = v[starti:]
            self.prices = (t,o,h,l,c,v)
            self._initCaches()
            self.nowidx -= starti
            self.now = t[self.nowidx]
            return starti
        except IndexError:
            lib.printError(self.now, "%s | self.now=%d self.nowidx=%d len(t)=%d starti=%d" % \
                           (self.name, self.now, self.nowidx, len(t), starti)
                           )

    def onTick(self, tickEvent):
        epoch = tickEvent.time
        (i, epoch) = self.getTime(epoch)
        if i < 0:
            return (-1, -1)
        #nshift = 0
        if epoch != self.now:
            self.now = epoch
            self.nowidx = i
            self.truncateOldFrom()
            
        return (self.nowidx, self.now)
        
            
    def getPrices(self, starti=0, endi=-1):
        if starti == -1:
            starti = 0
        (t,o,h,l,c,v) = self.prices
        if env.run_mode == env.MODE_SIMULATE:
            if endi == -1 and self.nowidx >= 0:
                endi = self.nowidx
        if endi == -1:
            endi = len(t)-1
        return (t[starti:endi+1],
                o[starti:endi+1],
                h[starti:endi+1],
                l[starti:endi+1],
                c[starti:endi+1],
                v[starti:endi+1])
            
            
    def getTime(self, epoch=-1):
        errret = (-1, -1)
        self.cache_used = False
        if epoch == -1:
            epoch = lib.nowepoch()
            
        epoch = epoch - (epoch % self.unitsecs)
        if epoch == self.now:
            return self.epochsidx[epoch], epoch
        
        (t,o,h,l,c,v) = self.prices
        if epoch > t[-1]:
            (t1,o1,h1,l1,c1,v1) = getterlib.getPrices(self.instrument, 
                            self.granularity, t[-1]+self.unitsecs, epoch)
            if len(t1) == 0:
                return (t[-1], len(t)-1)
            shiftt = len(t)
            for i in range(len(t1)):
                self.epochsidx[t1[i]] = i+shiftt
            (t,o,h,l,c,v) = self.prices
            t.extend(t1)
            o.extend(o1)
            h.extend(h1)
            l.extend(l1)
            c.extend(c1)
            v.extend(v1)
           
        if epoch not in self.epochsidx.keys():
            return errret
        
        return self.epochsidx[epoch], epoch
    
    