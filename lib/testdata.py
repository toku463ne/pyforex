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
                        direction):
    db = MSSQLDB()
    pricetbl = lib.names.getPriceTable(instrument, granularity)
    priceunit = tradelib.pip2Price(1, instrument)
    unitsecs = tradelib.getUnitSecs(granularity)
    start -= (start % unitsecs)
    end -= (end % unitsecs)
    
    curr = start
    price = startprice
    cnt = 0
    while curr < end:
        i = cnt % 3
        if i == 2:
            price -= 2*priceunit*direction
        else:
            price += 2*priceunit*direction
        sql = "insert into %s ([ep],[dt],[o],[h],[l],[c],[v]) \
            values (%d,'%s',%f,%f,%f,%f,%d)" % (
                pricetbl,
                curr, 
                lib.epoch2str(curr, "%Y-%m-%d %H:%M:%S"),
                price,
                price+4*priceunit*direction,
                price,
                price+4*priceunit*direction,
                (i+1)*10
                ) 
        db.execute(sql)
        curr += unitsecs
        cnt+=1
        
#
def prepare2legData(instrument, 
                        granularity, 
                        startprice,
                        start, 
                        end):
    reCreatePriceTable(instrument, granularity)
    midep = (start + end) / 2
    unitsecs = tradelib.getUnitSecs(granularity)
    insertMonoPricedata(instrument, granularity,
                        startprice,start,midep,1)
    insertMonoPricedata(instrument, granularity,
                        startprice,midep+unitsecs,end,-1)
    
        
if __name__ == "__main__":
    st = lib.str2epoch("2019-11-01T00:00:00")
    ed = lib.str2epoch("2019-11-01T00:30:00")
    instrument = "USD_JPY"
    granularity = "M5"
    reCreatePriceTable(instrument, granularity)
    insertMonoPricedata(instrument, granularity,100.0,st,ed,-1)
    print("finished")