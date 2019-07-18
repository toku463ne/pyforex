'''
Created on 2019/04/12

@author: kot
'''

from data_getter import DataGetter
import env

import v20
import json


class OandaGetter(DataGetter):
    def __init__(self,instrument, granularity, priceToGet="M"):
        '''
        price:
            M = Mid point
            B = Bid
            A = Ask
        '''
        self.name = "%s_%s" % (instrument, granularity)
        self.instrument = instrument
        self.granularity = granularity
        self.priceToGet = priceToGet
        
        oanda = env.conf["oanda"]
        self.api = v20.Context(oanda["hostname"], 
                               token=oanda["token"], 
                               datetime_format="UNIX")

        self.accountid = oanda["accountid"]
        
        
        
    def getPrice(self, startep, endep):
        price = self.priceToGet
        endep += 1
        
        res = self.api.pricing.candles(
            self.instrument,
            price=price,
            granularity=self.granularity,
            fromTime=startep,
            toTime=endep
            )
        if res.status != 200:
            return None, None, None, None, None, None
        
        candleType = ""
        if price == "M":
            candleType = "mid"
        if price == "B":
            candleType = "bid"
        if price == "A":
            candleType = "ask"
        
        cdls = res.body["candles"]
        count = len(cdls)
        (t, o, h, l, c, v) = self.getIniPriceLists(0, count)
        for i in range(count):
            cdl = cdls[i]
            item = cdl[candleType]
            t[i] = int(cdl["time"].split(".")[0])
            v[i] = cdl["volume"]
            o[i] = float(item["o"])
            h[i] = float(item["h"])
            l[i] = float(item["l"])
            c[i] = float(item["c"])
            
        return t, o, h, l, c, v
        
        
        
if __name__ == "__main__":
    o = OandaGetter("USD_JPY", "H1")
    import lib
    st = lib.str2epoch("2019/04/02 09:00", "%Y/%m/%d %H:%M")
    ed = lib.str2epoch("2019/04/02 12:00", "%Y/%m/%d %H:%M")
    
    t, o, h, l, c, v = o.getPrice(st, ed)
    print(t)
    print(v)
    print(o)
    
    