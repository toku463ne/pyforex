'''
Created on 2019/05/01

@author: kot
'''
import lib
import lib.tradelib as tradelib
from collections import OrderedDict
import lib.getter as getterlib
EP = 0
O = 1
H = 2
L = 3
C = 4
V = 5


class SubChart(object):
    def __init__(self, instrument, granularity, 
                 startep, endep=0, nbars=0, cachesize=1000):
        self.instrument = instrument
        self.granularity = granularity
        self.unitsecs = tradelib.getUnitSecs(granularity)
        self.cachesize = cachesize
        #self.maxsize = maxsize
        self.curr_time = 0
        self.epochsidx = OrderedDict()
        self.epochcache = OrderedDict()
        
        if endep > 0:
            (t,o,h,l,c,v) = getterlib.getPrices(instrument, 
                                                  granularity, startep, endep)
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
        self.startep = startep
        self.endep = endep
        self.now = startep
    
    
    
    def _initCaches(self):
        self.epochsidx = OrderedDict()
        self.epochcache = OrderedDict()
        t = self.prices[EP]
        for i in range(len(t)):
            self.epochsidx[t[i]] = i
    
    
    
    
    def getLatestChart(self, curr_last_epoch, end_epoch=-1):
        if end_epoch == -1:
            ep = min(lib.nowepoch(), self.endep)
        else:
            ep = min(lib.nowepoch(), self.endep, end_epoch)
        (t1,o1,h1,l1,c1,v1) = getterlib.getPrices(self.instrument, 
                            self.granularity, curr_last_epoch+1, ep)
        if len(t1) > 0:
            (t,o,h,l,c,v) = self.prices
            t.extend(t1)
            o.extend(o1)
            h.extend(h1)
            l.extend(l1)
            c.extend(c1)
            v.extend(v1)
        return (t1,o1,h1,l1,c1,v1)
    
    
    # returns number of shift
    def truncateOldFrom(self, starti):
        #epochi, _ = self.getTime(base_epoch)
        if starti <= 0:
            return 0
        (t,o,h,l,c,v) = self.prices
        t = t[starti:]
        o = o[starti:]
        h = h[starti:]
        l = l[starti:]
        c = c[starti:]
        v = v[starti:]
        self.prices = (t,o,h,l,c,v)
        self._initCaches()
        return starti
        
            
    def getPrices(self, start_i=-1, end_i=-1):
        (t,_,_,_,_,_) = self.prices
        if len(t)-1 <= end_i:
            end_i = len(t)-1
        if start_i == -1 and end_i == -1:
            return self.prices
        elif start_i == -1 and end_i > 0:
            return self.prices[:end_i]
        elif start_i > 0 and end_i == -1:
            return self.prices[start_i:]
        else:
            return self.prices[start_i:end_i+1]
    
    
    def getAt(self, idx):
        (t,o,h,l,c,v) = self.prices
        return (t[idx],o[idx],h[idx],
                l[idx],c[idx],v[idx])
            
            
    def getTime(self, epoch):
        epoch = epoch - (epoch % self.unitsecs)
        last_epoch = self.prices[EP][-1]
        if epoch > last_epoch:
            (t,_,_,_,_,_) = self.getLatestChart(last_epoch)
            if t[-1] + self.unitsecs < epoch:
                return -1,-1
            epoch = t[-1]
            
        epoch1 = epoch
        if epoch in self.epochsidx.keys():
            pass
        elif epoch1 in self.epochcache.keys():
            epoch = self.epochcache[epoch1]
        else:
            while epoch not in self.epochsidx.keys():
                epoch -= self.unitsecs
                if epoch < self.startep:
                    return (-1, -1)
            self.epochcache[epoch1] = epoch
            if len(self.epochcache) > self.cachesize:
                self.epochcache.popitem(last=False)
        return self.epochsidx[epoch], epoch
    
    def getTimeFromIdx(self, idx):
        return self.prices[EP][idx]
    