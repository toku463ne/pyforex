'''
Created on 2019/04/10

@author: kot
'''
import lib.tradelib as tradelib

import math

class DataGetter(object):
    
    def __init__(self, childDG):
        self.childDG = childDG
        self.unitsecs = childDG.unitsecs
        self.maxID = -1
        (self.ep,
         self.o,
         self.h,
         self.l,
         self.c,
         self.v) = self.getIniPriceLists(0, 0)
        
    
    def retrievePrice(self, startep, endep):
        (self.ep,
         self.o,
         self.h,
         self.l,
         self.c,
         self.v) = self.childDG.getPrice(startep, endep)
        
        
    def getPrice(self, startep, endep):
        if len(self.ep) == 0:
            return self.getIniPriceLists(0, 0)
        if startep < self.ep[0] or endep < self.ep[0] \
            or startep > self.ep[-1] or endep > self.ep[-1]:
            return self.getIniPriceLists(0, 0)
        
        sti = math.floor((startep - self.ep[0])/self.unit)
        edi = math.floor((endep - self.ep[0] - 1)/self.unit)
        return (self.ep[sti:edi+1],
                self.o[sti:edi+1],
                self.h[sti:edi+1],
                self.l[sti:edi+1],
                self.c[sti:edi+1],
                self.v[sti:edi+1])
        
    def getNPrice(self, endep, nbars):
        startep = endep - nbars*self.unitsecs
        (ep1, o1, h1, l1, c1, v1) = self.getPrice(startep, endep)
        if len(ep1) == nbars:
            return (ep1, o1, h1, l1, c1, v1)
        while len(ep1) < nbars:
            endep1 = startep-1
            startep = startep - 12*24*2*self.unitsecs
            (ep2, o2, h2, l2, c2, v2) = self.getPrice(startep, endep1)
            ep2.extend(ep1)
            o2.extend(o1)
            h2.extend(h1)
            l2.extend(l1)
            c2.extend(c1)
            v2.extend(v1)
            (ep1, o1, h1, l1, c1, v1) = (ep2, o2, h2, l2, c2, v2)
        sti = len(ep1)-nbars
        return (ep1[sti:], o1[sti:], h1[sti:], l1[sti:], c1[sti:], v1[sti:])
    
        
    def getPriceAt(self, pos):
        if pos >= len(self.ep):
            return -1,-1,-1,-1,-1,-1
        return (self.ep[pos],
                self.o[pos],
                self.h[pos],
                self.l[pos],
                self.c[pos],
                self.v[pos],)
        
    def getIniPriceLists(self, n, size):
        ep = [n]*size
        o = [n]*size
        h = [n]*size
        l = [n]*size
        c = [n]*size
        v = [n]*size
        return (ep, o, h, l, c, v)
    
if __name__ == "__main__":
    import env
    from data_getter.oanda import OandaGetter
    env.run_mode = env.MODE_UNITTEST
    from db.mssql import MSSQLDB
    from data_getter.mssql import MSSQLGetter
    from data_getter.oanda import OandaGetter
    import lib
    d = MSSQLDB()
    
    d.execute("drop table if exists USD_JPY_H1_prices;")
    d.execute("drop table if exists USD_JPY_H1_metainf;")
    
    og = DataGetter(MSSQLGetter(OandaGetter("USD_JPY", "H1")))
    st = lib.str2epoch("2019/04/02 09:00", "%Y/%m/%d %H:%M")
    ed = lib.str2epoch("2019/04/02 17:00", "%Y/%m/%d %H:%M")
    
    og.retrievePrice(st, ed)
    
    st = lib.str2epoch("2019/04/02 11:00", "%Y/%m/%d %H:%M")
    ed = lib.str2epoch("2019/04/02 13:00", "%Y/%m/%d %H:%M")
    (t, o,h,l,c,v) = og.getPrice(st, ed)
    print(t)
    print(o)
