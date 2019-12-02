'''
Created on 2019/11/14

@author: kot
'''

import env
import lib
import lib.names
import lib.tradelib as tradelib
env.run_mode = env.MODE_UNITTEST
from db.mssql import MSSQLDB
    
    
def reCreatePriceTable(instrument, 
                        granularity):
    pricetbl = lib.names.getPriceTable(instrument, granularity)
    db = MSSQLDB()
    db.execute("drop table if exists %s;" % pricetbl)
    db.createTable(pricetbl, "prices")
    
def insertMonoPricedata(instrument, 
                        granularity, 
                        startprice,
                        start, 
                        end,
                        direction,
                        pipdiff):
    db = MSSQLDB()
    pricetbl = lib.names.getPriceTable(instrument, granularity)
    priceunit = tradelib.pip2Price(1, instrument)
    unitsecs = tradelib.getUnitSecs(granularity)
    start -= (start % unitsecs)
    end -= (end % unitsecs)
    
    curr = start
    price = startprice
    cnt = 0
    while curr <= end:
        i = cnt % 3
        if i == 2:
            price -= pipdiff*priceunit*direction
        else:
            price += pipdiff*priceunit*direction
        if direction == 1:
            o = price
            c = price+2*pipdiff*priceunit
        else:
            o = price+2*pipdiff*priceunit
            c = price
        sql = "insert into %s ([ep],[dt],[o],[h],[l],[c],[v]) \
            values (%d,'%s',%f,%f,%f,%f,%d)" % (
                pricetbl,
                curr, 
                lib.epoch2str(curr, "%Y-%m-%d %H:%M:%S"),
                o,
                price+2*pipdiff*priceunit,
                price,
                c,
                (i+1)*10
                ) 
        db.execute(sql)
        curr += unitsecs
        cnt+=1
 
def makeSmallPeriodData(instrument, large_period, small_period):
    reCreatePriceTable(instrument, small_period)
    lus = tradelib.getUnitSecs(large_period)
    sus = tradelib.getUnitSecs(small_period)
    if lus <= sus:
        raise Exception("large_period must be greater than small_period!")
    db = MSSQLDB()
    lpricetbl = lib.names.getPriceTable(instrument, large_period)
    spricetbl = lib.names.getPriceTable(instrument, small_period)
    diffrate = lus/sus
    
    cnt = db.countTable(lpricetbl)
    if cnt == 0:
        raise Exception("No data in %s" % lpricetbl)
    
    
    for (ep,o,h,l,c,v) in db.execute("select ep,o,h,l,c,v from %s;" % lpricetbl).fetchall():
        bar_size = (h-l)/diffrate
        pdiff = (h-l-bar_size)/diffrate
        if c > o:
            direction = 1
            price = l
        else:
            direction = -1
            price = h

        vs = int(v/diffrate)
        for i in range(int(diffrate)):
            os = price
            if direction == 1:
                hs = price + bar_size
                ls = os
                cs = hs
            else:
                hs = price
                ls = price - bar_size
                cs = ls
            
            if i >= diffrate-1:
                if direction == 1:
                    hs = h
                    cs = h
                else:
                    ls = l
                    cs = l
            
            sql = "insert into %s ([ep],[dt],[o],[h],[l],[c],[v]) \
            values (%d,'%s',%f,%f,%f,%f,%d)" % (
                spricetbl,
                ep, 
                lib.epoch2str(ep, "%Y-%m-%d %H:%M:%S"),
                os,hs,ls,cs,vs
                )
            db.execute(sql)
                
            shuff = i % 4
            if shuff == 2:
                price -= direction*pdiff
            elif shuff == 3:
                price += direction*pdiff*2
            else:
                price += direction*pdiff 
        
            ep += sus
    
    
        
#
def prepare2legData(instrument, 
                        granularity, 
                        startprice,
                        start, 
                        end,
                        diffpips):
    reCreatePriceTable(instrument, granularity)
    midep = (start + end) / 2
    unitsecs = tradelib.getUnitSecs(granularity)
    insertMonoPricedata(instrument, granularity,
                        startprice,start,midep,1,diffpips)
    insertMonoPricedata(instrument, granularity,
                        startprice,midep+unitsecs,end,-1,diffpips)
    
        
if __name__ == "__main__":
    st = lib.str2epoch("2019-11-01T00:00:00")
    ed = lib.str2epoch("2019-11-01T00:30:00")
    instrument = "USD_JPY"
    granularity = "M5"
    granularity2 = "M1"
    reCreatePriceTable(instrument, granularity)
    reCreatePriceTable(instrument, granularity2)
    insertMonoPricedata(instrument, granularity,100.0,st,ed,-1, 2)
    makeSmallPeriodData(instrument, granularity, granularity2)
    print("finished")