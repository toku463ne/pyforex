'''
Created on 2019/04/10

@author: kot
'''
from data_getter import DataGetter
import lib.names
from db.mssql import MSSQLDB
import lib.tradelib as tradelib

N_REQUEST_ROWS = 100

class MSSQLGetter(DataGetter):

    def __init__(self, childDG):
        self.instrument = childDG.instrument
        self.granularity = childDG.granularity
        self.unitsecs = tradelib.getUnitSecs(self.granularity)
        self.childDG = childDG
        self.metatbl = lib.names.getMetainfTable(self.instrument, self.granularity)
        self.pricetbl = lib.names.getPriceTable(self.instrument, self.granularity)
        self.db = MSSQLDB()
        self.db.createTable(self.metatbl, "metainf")
        self.db.createTable(self.pricetbl, "prices")
        self.maxID = -1
        self.metainf = {}
        self.getMetaInf()
        

    def getMetaInf(self):
        cur = self.db.execute("select id, startep, endep \
                            from %s;" % self.metatbl)
        for row in cur.fetchall():
            if row.id > self.maxID:
                self.maxID = row.id
            self.metainf[row.id] = [row.id, row.startep, row.endep]

    
    def insertMetaInf(self, oids):
        if len(oids) == 0:
            return
        for oid in oids:
            m = self.metainf[oid]
            sql = "insert into %s (id, startep, endep, startdt, enddt) \
            values (?,?,?,?,?);" % (self.metatbl)
            self.db.execute(sql, (oid, m[1], m[2],
                         lib.epoch2dt(m[1]), lib.epoch2dt(m[2])))

    
    def updateMetaInf(self, oids):
        if len(oids) == 0:
            return
        for oid in oids:
            m = self.metainf[oid]
            sql = "update %s set startep=?, endep=?, startdt=?, enddt=? where id=%d;" % \
                        (self.metatbl, oid)
            self.db.execute(sql, 
                            (m[1], m[2], lib.epoch2dt(m[1]), lib.epoch2dt(m[2])))
        
    
    def deleteMetaInf(self, oids):
        if len(oids) == 0:
            return
        moids = map(str, oids)
        sql = "delete from %s where id in (%s)" % (self.metatbl, ",".join(moids))
        self.db.execute(sql)
        
        
    def insertData(self, ep,o,h,l,c,v):
        sql = ""
        for i in range(len(ep)):
            sql = "%sinsert into %s ([ep],[o],[h],[l],[c],[v]) \
                values (%s,%s,%s,%s,%s,%s);" % \
                (sql, self.pricetbl, ep[i],o[i],h[i],l[i],c[i],v[i])
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
        
    def _getPriceFromChild(self, startep, endep):
        (ep,o,h,l,c,v) = self.childDG.getPrice(startep, endep)
        if len(ep) == 0:
            return (0, 0)
        try:
            self.insertData(ep, o, h, l, c, v)
        except Exception as  e:
            sqlstate = e.args[0]
            if sqlstate == '23000':
                lib.printInfo(ep[0], str(e))
            else:
                raise e
        return (ep[0], ep[-1])
        
        
    def _getSortedMetaList(self):
        mList = []
        for k in self.metainf.keys():
            mList.append(self.metainf[k])
        
        def _getMin(m):
            return m[1]
        mList.sort(key=_getMin)
        return mList
    
    def updateMaxID(self):
        self.maxID += 1
        return self.maxID
        
    
    def getPrice(self, startep, endep):
        interval_secs = self.unitsecs * N_REQUEST_ROWS
        (ep,o,h,l,c,v) = ([],[],[],[],[],[])
        baseep = startep
        while baseep <= endep:
            lastep = min(endep,baseep+interval_secs)
            (ep1,o1,h1,l1,c1,v1) = self._getPriceProc(baseep, lastep)
            ep.extend(ep1)
            o.extend(o1)
            h.extend(h1)
            l.extend(l1)
            c.extend(c1)
            v.extend(v1)
            baseep += interval_secs + self.unitsecs
        return (ep,o,h,l,c,v)
        
    def _getPriceProc(self, startep, endep):
        startep = tradelib.getNearEpoch(self.granularity, startep)
        endep = tradelib.getNearEpoch(self.granularity, endep)
            
        if len(self.metainf) == 0:
            (_, _) = self._getPriceFromChild(startep, endep)
            (ep, o, h, l, c, v) = self.selectData(startep, endep)
            if len(ep) == 0:
                return (ep, o, h, l, c, v)
            oid = self.updateMaxID()
            self.metainf[oid] = [oid, startep, endep]
            self.insertMetaInf([oid])
            return (ep, o, h, l, c, v)
        
        mList = self._getSortedMetaList()
        
        updates = {}
        inserts = {}
        deletes = {}
        newstart = startep
        oldid = -1
        i = 0
        startID = -1
        endID = -1
        oid = -1
        for m in mList:
            mstart = m[1]
            mend = m[2]
            mid = m[0]
            
            if endep < mstart:
                (_, _) = self._getPriceFromChild(newstart, endep)
                st = newstart
                ed = endep
                if st == 0:
                    break
                if startep < newstart or \
                    (oldid >= 0 and newstart - self.unitsecs - 1 <= mend):
                    self.metainf[oldid][2] = ed
                    endID = oldid
                    updates[oldid] = 1
                else:
                    oid = self.updateMaxID()
                    self.metainf[oid] = [oid, st, ed]
                    inserts[oid] = 1
                    startID = oid
                    endID = oid
                break
            if newstart < mstart and mstart <= endep:
                (_, _) = self._getPriceFromChild(newstart, mstart-1)
                st = newstart
                ed = tradelib.getNearEpoch(self.granularity, mstart-1)
                if st == 0:
                    pass
                elif startep < newstart:
                    self.metainf[oldid][2] = ed
                    updates[oldid] = 1
                else:
                    if oldid >= 0 and oldid > mid:
                        oldst = self.metainf[oldid][1]
                        if st > oldst:
                            st = oldst
                            
                    
                    self.metainf[mid][1] = st
                    updates[mid] = 1
                    startID = mid
                    
                    
                        
            if newstart <= mend and mend < endep and i < len(mList)-1:
                if newstart == startep:
                    startID = mid
                newstart = mend+self.unitsecs+1
                
            if i >= len(mList)-1:
                if newstart <= mend and mend < endep:
                    (_, _) = self._getPriceFromChild(mend+self.unitsecs, endep)
                    st = tradelib.getNearEpoch(self.granularity, mend+self.unitsecs)
                    ed = endep
                    if st > 0:
                        self.metainf[mid][2] = ed
                        updates[mid] = 1
                    if startep == newstart:
                        startID = mid
                    endID = mid
                if newstart > mend:
                    (_, _) = self._getPriceFromChild(startep, endep)
                    st = startep
                    ed = endep
                    if st > 0:
                        oid = self.updateMaxID()
                        self.metainf[oid] = [oid, st, ed]
                        inserts[oid] = 1
                        startID = oid
                        endID = oid
            if endep <= mend:
                endID = oid
                break
            i += 1
            oldid = mid
        
        mList = self._getSortedMetaList()
        firstm = None
        oldm = None
        mIndex = {}
        for j in range(len(mList)):
            mIndex[mList[j][0]] = j
        
        for m in mList:
            mid = m[0]
            mstart = m[1]
            mend = m[2]
            if startID == mid:
                if oldm != None and oldm[2]+self.unitsecs>=mstart:
                    firstm = oldm
                else:
                    firstm = m
                    continue
            if firstm == None:
                continue
            
            if startID >= 0 and mstart >= mList[mIndex[startID]][1] \
                and firstm[2]+self.unitsecs>=mstart:
                
                firstm[2] = max(mend, firstm[2])
                del self.metainf[mid]
                deletes[mid] = 1
                updates[mid] = 0
                inserts[mid] = 0
            if endID == mid:
                break
            oldm = m
        mList = None
        
        self.deleteMetaInf(deletes.keys())
        updList = []
        for oid in updates.keys():
            if updates[oid] == 1:
                updList.append(oid)
        self.updateMetaInf(updList)
        insList = []
        for oid in inserts.keys():
            if inserts[oid] == 1:
                insList.append(oid)
        self.insertMetaInf(insList)
        
        (ep, o, h, l, c, v) = self.selectData(startep, endep)
        return (ep, o, h, l, c, v)
    

    
if __name__ == "__main__":
    import env
    from data_getter.oanda import OandaGetter
    env.run_mode = env.MODE_UNITTEST
    from db.mssql import MSSQLDB
    d = MSSQLDB()
    
    d.execute("drop table if exists USD_JPY_M1_prices;")
    d.execute("drop table if exists USD_JPY_M1_metainf;")
    
    og = MSSQLGetter(OandaGetter("USD_JPY", "M1"))
    st = lib.str2epoch("2019/04/01 00:10", "%Y/%m/%d %H:%M")
    ed = lib.str2epoch("2019/04/01 00:15", "%Y/%m/%d %H:%M")
    t, o, h, l, c, v = og.getPrice(st, ed)
    
    
    og = MSSQLGetter(OandaGetter("USD_JPY", "M1"))
    st = lib.str2epoch("2019/03/31 23:55", "%Y/%m/%d %H:%M")
    ed = lib.str2epoch("2019/04/01 00:00", "%Y/%m/%d %H:%M")
    t, o, h, l, c, v = og.getPrice(st, ed)
    
    og = MSSQLGetter(OandaGetter("USD_JPY", "M1"))
    st = lib.str2epoch("2019/04/01 00:00", "%Y/%m/%d %H:%M")
    ed = lib.str2epoch("2019/04/01 00:05", "%Y/%m/%d %H:%M")
    t, o, h, l, c, v = og.getPrice(st, ed)
    
    og = MSSQLGetter(OandaGetter("USD_JPY", "M1"))
    st = lib.str2epoch("2019/04/01 00:05", "%Y/%m/%d %H:%M")
    ed = lib.str2epoch("2019/04/01 00:15", "%Y/%m/%d %H:%M")
    t, o, h, l, c, v = og.getPrice(st, ed)
    
    
    
    d.execute("drop table if exists USD_JPY_H1_prices;")
    d.execute("drop table if exists USD_JPY_H1_metainf;")
    
    og = MSSQLGetter(OandaGetter("USD_JPY", "H1"))
    st = lib.str2epoch("2019/04/02 09:00", "%Y/%m/%d %H:%M")
    ed = lib.str2epoch("2019/04/02 12:00", "%Y/%m/%d %H:%M")
    t, o, h, l, c, v = og.getPrice(st, ed)
    st = lib.str2epoch("2019/04/02 15:00", "%Y/%m/%d %H:%M")
    ed = lib.str2epoch("2019/04/02 17:00", "%Y/%m/%d %H:%M")
    t, o, h, l, c, v = og.getPrice(st, ed)
    st = lib.str2epoch("2019/04/02 07:00", "%Y/%m/%d %H:%M")
    ed = lib.str2epoch("2019/04/02 10:00", "%Y/%m/%d %H:%M")
    t, o, h, l, c, v = og.getPrice(st, ed)
    st = lib.str2epoch("2019/04/02 14:00", "%Y/%m/%d %H:%M")
    ed = lib.str2epoch("2019/04/02 15:00", "%Y/%m/%d %H:%M")
    t, o, h, l, c, v = og.getPrice(st, ed)
    st = lib.str2epoch("2019/04/02 17:00", "%Y/%m/%d %H:%M")
    ed = lib.str2epoch("2019/04/02 19:00", "%Y/%m/%d %H:%M")
    t, o, h, l, c, v = og.getPrice(st, ed)
    st = lib.str2epoch("2019/04/02 10:00", "%Y/%m/%d %H:%M")
    ed = lib.str2epoch("2019/04/02 20:00", "%Y/%m/%d %H:%M")
    t, o, h, l, c, v = og.getPrice(st, ed)
    
    
    print("Finished")
    