'''
Created on 2019/04/12

@author: kot
'''

from data_getter import DataGetter
from tools.oanda import OandaWrapper

from oandapyV20.endpoints.instruments import InstrumentsCandles
import lib


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
        
        self.oandaw = OandaWrapper()
        
        
    def getPrice(self, startep, endep):
        price = self.priceToGet
        endep += 1
        candleType = ""
        if price == "M":
            candleType = "mid"
        if price == "B":
            candleType = "bid"
        if price == "A":
            candleType = "ask"
        
        #lib.epoch2str(startep, "%Y-%m-%dT%H:%M:%SZ")
        (t, o, h, l, c, v) = self.getIniPriceLists(0, 0)
        req = InstrumentsCandles(instrument="USD_JPY", params={
            "granularity": self.granularity,
            "from": lib.epoch2str(startep, "%Y-%m-%dT%H:%M:%SZ"),
            "to": lib.epoch2str(endep, "%Y-%m-%dT%H:%M:%SZ"),
            "datetime_format": "UNIX"})
        self.oandaw.request(req)
        cdls = req.response.get('candles')
        count = len(cdls)
        (t, o, h, l, c, v) = self.getIniPriceLists(0, count)
        for i in range(count):
            cdl = cdls[i]
            item = cdl[candleType]
            ti = cdl["time"].split(".")[0]
            t[i] = lib.str2epoch(ti, "%Y-%m-%dT%H:%M:%S")
            v[i] = cdl["volume"]
            o[i] = float(item["o"])
            h[i] = float(item["h"])
            l[i] = float(item["l"])
            c[i] = float(item["c"])
    
        
        '''
        for req in InstrumentsCandlesFactory(instrument=self.instrument, params={
            "granularity": self.granularity,
            "from": lib.epoch2str(startep, "%Y-%m-%dT%H:%M:%SZ"),
            "to": lib.epoch2str(endep, "%Y-%m-%dT%H:%M:%SZ"),
            "datetime_format": "UNIX"}):
            
            self.oandaw.request(req)
            cdls = req.response.get('candles')
            count = len(cdls)
            (t1, o1, h1, l1, c1, v1) = self.getIniPriceLists(0, count)
            for i in range(count):
                cdl = cdls[i]
                item = cdl[candleType]
                ti = cdl["time"].split(".")[0]
                t1[i] = lib.str2epoch(ti, "%Y-%m-%dT%H:%M:%S")
                v1[i] = cdl["volume"]
                o1[i] = float(item["o"])
                h1[i] = float(item["h"])
                l1[i] = float(item["l"])
                c1[i] = float(item["c"])
            t.extend(t1)
            v.extend(v1)
            o.extend(o1)
            h.extend(h1)
            l.extend(l1)
            c.extend(c1)
        '''
         
        return t, o, h, l, c, v
        
        
        
if __name__ == "__main__":
    o = OandaGetter("USD_JPY", "M5")
    import lib
    st = lib.str2epoch("2019/04/04 11:50", "%Y/%m/%d %H:%M")
    ed = lib.str2epoch("2019/04/04 12:20", "%Y/%m/%d %H:%M")
    
    t, o, h, l, c, v = o.getPrice(st, ed)
    print(t)
    print(v)
    print(o)
    
    