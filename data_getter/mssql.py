'''
Created on 2019/11/13

@author: kot
'''
from data_getter import DataGetter
import lib.names
from db.mssql import MSSQLDB
import lib.tradelib as tradelib
import env

N_REQUEST_ROWS = 100

class MSSQLGetter(DataGetter):

    def __init__(self, childDG):
        self.instrument = childDG.instrument
        self.granularity = childDG.granularity
        self.unitsecs = tradelib.getUnitSecs(self.granularity)
        self.childDG = childDG
        self.pricetbl = lib.names.getPriceTable(self.instrument, self.granularity)
        self.db = MSSQLDB()
        self.db.createTable(self.pricetbl, "prices")
        self.maxID = -1
        
    def insertData(self, ep,o,h,l,c,v):
        sql = ""
        for i in range(len(ep)):
            sql = "%sinsert into %s ([ep],[dt],[o],[h],[l],[c],[v]) \
                values (%s,'%s', %s,%s,%s,%s,%s);" % \
                (sql, self.pricetbl, 
                 ep[i],
                 lib.epoch2str(ep[i],env.DATE_FORMAT_NORMAL2),
                 o[i],h[i],l[i],c[i],v[i])
            if i >= N_REQUEST_ROWS and i % N_REQUEST_ROWS == 0:
                self.db.execute(sql)
                sql = ""
        self.db.execute(sql)
        
        
    def selectData(self, startep, endep):
        sql = "select ep,o,h,l,c,v from %s where ep>=%d and ep<=%d" % \
            (self.pricetbl, startep, endep)
        cur = self.db.execute(sql)
        rows = cur.fetchall()
        (ep, o, h, l, c, v) = self.getIniPriceLists(0, len(rows))
        i = 0
        for row in rows:
            ep[i] = row.ep
            o[i] = row.o
            h[i] = row.h
            l[i] = row.l
            c[i] = row.c
            v[i] = row.v
            i += 1
        return (ep, o, h, l, c, v)
    
    def getEpEdges(self):
        sql = "select min(ep), max(ep) from %s;" % (self.pricetbl)
        cur = self.db.execute(sql)
        if cur == None:
            return (-1, -1)
        res = cur.fetchone()
        if res == None:
            return (-1, -1)
        (mi, ma) = res
        if mi == None:
            return (-1, -1)
        return (mi, ma)
        
    '''
    def _getPriceFromChild(self, startep, endep):
        (ep,o,h,l,c,v) = self.childDG.getPrice(startep, endep)
        if len(ep) == 0:
            return ([],[],[],[],[],[])
        try:
            self.insertData(ep, o, h, l, c, v)
        except Exception as  e:
            sqlstate = e.args[0]
            if sqlstate == '23000':
                lib.printInfo(ep[0], str(e))
            else:
                raise e
        lib.log("Data from child. %s - %s - %d rows" % (
                lib.epoch2str(startep, env.DATE_FORMAT_NORMAL), 
                lib.epoch2str(endep, env.DATE_FORMAT_NORMAL),
                len(ep)
            ))
        return (ep,o,h,l,c,v)
    '''
   
    def _getPriceFromChild(self, startep, endep):
        interval_secs = self.unitsecs * N_REQUEST_ROWS
        (ep,o,h,l,c,v) = ([],[],[],[],[],[])
        baseep = startep
        while True:
            lastep = min(endep,baseep+interval_secs)
            (ep1,o1,h1,l1,c1,v1) = self.childDG.getPrice(baseep, lastep)
            ep.extend(ep1)
            o.extend(o1)
            h.extend(h1)
            l.extend(l1)
            c.extend(c1)
            v.extend(v1)
            if lastep >= endep:
                break;
            baseep += interval_secs + self.unitsecs
            
        if len(ep) == 0:
            return ([],[],[],[],[],[])
        try:
            self.insertData(ep, o, h, l, c, v)
        except Exception as e:
            sqlstate = e.args[0]
            if sqlstate == '23000':
                lib.printInfo(ep[0], str(e))
            else:
                raise e
        lib.log("Data from child. %s - %s - %d rows" % (
                lib.epoch2str(startep, env.DATE_FORMAT_NORMAL), 
                lib.epoch2str(endep, env.DATE_FORMAT_NORMAL),
                len(ep)
            ))
        return (ep,o,h,l,c,v)
    
    '''
    def getPrice(self, startep, endep):
        interval_secs = self.unitsecs * N_REQUEST_ROWS
        (ep,o,h,l,c,v) = ([],[],[],[],[],[])
        baseep = startep
        while True:
            lastep = min(endep,baseep+interval_secs)
            (ep1,o1,h1,l1,c1,v1) = self._getPriceProc(baseep, lastep)
            ep.extend(ep1)
            o.extend(o1)
            h.extend(h1)
            l.extend(l1)
            c.extend(c1)
            v.extend(v1)
            if lastep >= endep:
                break;
            baseep += interval_secs + self.unitsecs
        return (ep,o,h,l,c,v)
    '''
    
    def getPrice(self, startep, endep):
        startep = tradelib.getNearEpoch(self.granularity, startep)
        endep = tradelib.getNearEpoch(self.granularity, endep)
        
        (mi, ma) = self.getEpEdges()
    
        if mi < 0:
            return self._getPriceFromChild(startep, endep)
    
        if mi > startep:
            self._getPriceFromChild(startep, mi-self.unitsecs)
        
        if ma < endep:
            self._getPriceFromChild(ma+self.unitsecs, endep)
        
        return self.selectData(startep, endep)
    
    
if __name__ == "__main__":
    import env
    from data_getter.oanda import OandaGetter
    env.run_mode = env.MODE_UNITTEST
    from db.mssql import MSSQLDB
    d = MSSQLDB()
    
    
    g = MSSQLGetter(OandaGetter("USD_JPY", "M1"))
    (ma, mi) = g.getEpEdges()
    print(ma)
        