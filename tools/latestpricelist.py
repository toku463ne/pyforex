'''
Created on 2019/07/05

@author: kot
'''
from lib import tradelib
import lib

class LatestPriceList(object):
    
    def __init__(self, life_secs, instrument):
        self.priceInfo = {}
        self.life_secs = life_secs
        self.decimalPlace = tradelib.getDecimalPlace(instrument)
        
    def upsert(self, epoch, price, obj):
        price = lib.truncFromDecimalPlace(price,
                                         self.decimalPlace)
        if price in self.priceInfo.keys():
            cnt = self.priceInfo[price].cnt + 1
        else:
            cnt = 1
            
        self.priceInfo[price] = PriceBox(epoch, price, obj, cnt)
        
        
        for price2 in list(self.priceInfo.keys()):
            if self.priceInfo[price2].epoch + self.life_secs < epoch:
                del self.priceInfo[price2]
        
        
        
    def searchObj(self, price):
        price = lib.truncFromDecimalPlace(price,
                                         self.decimalPlace)
        if price in self.priceInfo.keys():
            box = self.priceInfo[price]
            return box.obj, box.cnt
        return None, 0

    def searchNearest(self, price):
        upper_price = -1
        lower_price = -1
        for price2 in sorted(self.priceInfo.keys()):
            if price <= price2:
                upper_price = price2
                break
            lower_price = price2
        return (lower_price, upper_price)
    
    
class PriceBox(object):
    def __init__(self, epoch, price, obj, cnt=1):
        self.epoch = epoch
        self.price = price
        self.obj = obj
        self.cnt = cnt

    


        