'''
Created on 2019/05/06

@author: kot
'''
from ticker import Ticker
from event.tick import TickEvent

import lib
import lib.tradelib as tradelib
from tools.oanda import OandaWrapper
import env

from oandapyV20.endpoints.instruments import InstrumentsCandles

import time

EP = 0
O = 1
H = 2
L = 3
C = 4
V = 5

class LastOandaCandleTicker(Ticker):

    def __init__(self, instrument, granularity="M1"):
        #self.now = tradelib.getNearEpoch(granularity, lib.nowepoch())
        self.now = -1
        self.instrument = instrument
        self.granularity = granularity
        self.oandaw = OandaWrapper()
        self.ticker_type = env.TICKTYPE_ONLINE
        self.unitsecs = tradelib.getUnitSecs(granularity)
        
        
    def tick(self):
        
        candles = {}
        for price_comp in ["M", "B", "A"]:
            params = {"count": 1, 
                      "granularity": self.granularity, 
                      "price": price_comp}
            req = InstrumentsCandles(instrument=self.instrument, params=params)
            self.oandaw.request(req)
            if req.response == None:
                return None
            ds = req.response.get('candles')
            if len(ds) == 0:
                return None
            d = ds[-1]
            candles["time"] = d["time"]
            if price_comp == "M":
                price_name = "mid"
            if price_comp == "B":
                price_name = "bid"
            if price_comp == "A":
                price_name = "ask"
            
            candles["volume"] = d["volume"]
            candles[price_comp] = d[price_name]
        
        ti = candles["time"].split(".")[0]
        newepoch = lib.str2epoch(ti, "%Y-%m-%dT%H:%M:%S")
        if newepoch < self.now:
            return None
        #(t,_,h,l,c,_) = self.dataGetter.getPriceAt(self.pos)
        t = newepoch
        v = candles["volume"]
        p = candles["B"]
        (hb,lb,cb) = (float(p["h"]), float(p["l"]), float(p["c"]))
        p = candles["A"]
        (ha,la,ca) = (float(p["h"]), float(p["l"]), float(p["c"]))
        p = candles["M"]
        (o,h,l,c) = (float(p["o"]), float(p["h"]), float(p["l"]), float(p["c"]))
        
        
        updated = t!=self.now
        self.now = t
        if updated:
            return TickEvent(t, (ha+la+ca)/3, 
                             (hb+lb+cb)/3, o=o, h=h, l=l, c=c,v=v)
        else:
            time.sleep(self.unitsecs/2)
            return None
    
  
if __name__ == "__main__":
    loc = LastOandaCandleTicker("USD_JPY", "M5")
    te = loc.tick()
    print(te)