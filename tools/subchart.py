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
                 nbars=0, maxsize=12*24*3, truncateOld=True):
        self.name = name
        self.instrument = instrument
        self.granularity = granularity
        self.truncateOld = truncateOld
        self.unitsecs = tradelib.getUnitSecs(granularity)
        self.epochsidx = None
        self.nowidx = -1
        self.now = -1
        self.maxsize = maxsize
        self.size_to_cleanup = int(maxsize*1.5)
        
        if endep == -1:
            endep = lib.nowepoch()
        if startep == -1:
            startep = min(endep, lib.nowepoch())
        startep = startep - (startep % self.unitsecs) - self.unitsecs
        (t,o,h,l,c,v) = getterlib.getPrices(instrument, 
                                            granularity, startep, endep)
        if nbars > 0:
            (t1,o1,h1,l1,c1,v1) = getterlib.getNPrices(instrument, 
                                                       granularity, startep-1, nbars)
            nbars = len(t1)
            t1.extend(t)
            o1.extend(o)
            h1.extend(h)
            l1.extend(l)
            c1.extend(c)
            v1.extend(v)
            (t,o,h,l,c,v) = (t1,o1,h1,l1,c1,v1)
        self.prices = (t,o,h,l,c,v)
        
        self._initCaches()
        
        self.now = t[nbars]
        self.nowidx = nbars
        
        
    
    def _initCaches(self):
        self.epochsidx = OrderedDict()
        t = self.prices[EP]
        for i in range(len(t)):
            self.epochsidx[t[i]] = i
        
    # returns number of shift
    def truncateOldFrom(self):
        if self.truncateOld == False:
            return -1
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
            raise IndexError

    def onTick(self, tickEvent):
        epoch = tickEvent.time
        (i, epoch) = self.getTime(epoch, False)
        if i < 0:
            return -1
        #nshift = 0
        if epoch != self.now:
            self.now = epoch
            self.nowidx = i
            self.truncateOldFrom()
            
        return self.now
        
            
    def getPrices(self, startep=-1, endep=-1, nbars=0):
        starti = 0
        endi = -1
        if startep > 0:
            starti, startep = self.getTime(startep)
            starti = max(0, starti-nbars)
        if starti == -1:
            starti = 0
        if endep > 0:
            endi, endep = self.getTime(endep)
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
    
    def getMax(self, startep=-1, endep=-1):
        prices = self.getPrices(startep, endep)
        (tl,_,hl,_,_,_) = prices
        mav = 0
        mat = 0
        for i in range(len(hl)):
            if hl[i] > mav:
                mav = hl[i]
                mat = tl[i]
        return (mat, mav)
        
    def getMin(self, startep=-1, endep=-1):
        prices = self.getPrices(startep, endep)
        (tl,_,_,ll,_,_) = prices
        miv = 0
        mit = 0
        for i in range(len(ll)):
            if ll[i] < miv or miv == 0:
                miv = ll[i]
                mit = tl[i]
        return (mit, miv)
    
    def getNPrices(self, endep, nbars):
        endi, endep = self.getTime(endep)
        starti = max(0, endi-nbars+1)
        (t,o,h,l,c,v) = self.prices
        return (t[starti:endi+1],
                o[starti:endi+1],
                h[starti:endi+1],
                l[starti:endi+1],
                c[starti:endi+1],
                v[starti:endi+1])
    
    def getBarDiff(self, epoch1, epoch2):
        i1, _ = self.getTime(epoch1)
        i2, _ = self.getTime(epoch2)
        return max(i2-i1, 0)
    
    def getBeforeNPrice(self, epoch, nbars):
        i, _ = self.getTime(epoch)
        j = max(0, i - nbars)
        (t,o,h,l,c,v) = self.prices
        return (t[j],o[j],h[j],l[j],c[j],v[j])
    
    def getBeforeNt(self, epoch, nbars):
        (t,_,_,_,_,_) = self.getBeforeNPrice(epoch, nbars)
        return t
    
    
    def getNow(self):
        #return (self.nowidx, self.now)
        return self.now
            
            
    def getPrice(self, i=0):
        #j = self.nowidx - i
        if i == 0:
            j = self.nowidx
        else:
            j = i
        if j < 0:
            return (-1,-1,-1,-1,-1,-1)
        (t,o,h,l,c,v) = self.prices
        return (t[j],o[j],h[j],l[j],c[j],v[j])
            
    # if protected == False, base time subchart 
    def getTime(self, epoch=-1, protected=True):
        errret = (-1, -1)
        self.cache_used = False
        if epoch == -1:
            epoch = lib.nowepoch()
            
        if protected:
            epoch = epoch - (epoch % self.unitsecs)
            if epoch >= self.now:
                epoch = self.now
        else:
            epoch = epoch - (epoch % self.unitsecs) - self.unitsecs
        #epoch = epoch - (epoch % self.unitsecs)
        if epoch == self.now:
            return self.epochsidx[epoch], epoch
        
        (t,o,h,l,c,v) = self.prices
        if epoch > t[-1]:
            (t1,o1,h1,l1,c1,v1) = getterlib.getPrices(self.instrument, 
                            self.granularity, t[-1]+self.unitsecs, epoch)
            if len(t1) == 0:
                return (len(t)-1, t[-1])
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
    
    