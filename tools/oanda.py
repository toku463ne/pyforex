'''
Created on 2019/05/03

@author: kot
'''
import env
import lib
import oandapyV20
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.pricing as pricing

from oandapyV20.contrib.requests import (
    MarketOrderRequest,
    TakeProfitDetails,
    StopLossDetails
)

from oandapyV20.endpoints.trades import (
    TradeDetails,
    TradesList
    )

from oandapyV20.endpoints.transactions import (
    TransactionDetails,
    TransactionsSinceID
    )

class OandaWrapper(object):
    def __init__(self):
        oanda = env.conf["oanda"]
        self.accountID = oanda["accountid"]
        self.token = oanda["token"]
        self.api = oandapyV20.API(access_token=oanda["token"],
                                  environment=oanda["environment"])
        
    def request(self, req):
        try:
            if req == None:
                lib.printError(lib.nowepoch(), "req is None")
            res = self.api.request(req)
            return res
        except oandapyV20.exceptions.V20Error as err:
            lib.printError(lib.nowepoch(), "%s" % (str(err)))
        return None
            
                
    def getCurrPrice(self, instrument):
        r = pricing.PricingInfo(accountID=self.accountID, 
                                params={"instruments": instrument})
        rv = self.request(r)
        priced = rv["prices"][0]
        if instrument != priced["instrument"]:
            return -1,-1
        bid = priced["bids"][-1]["price"]
        ask = priced["asks"][-1]["price"]
        return float(bid), float(ask)
        
        
    def createMarketOrder(self, instrument, units, 
                    takeprofit_price=0, stoploss_price=0):
        if takeprofit_price == 0:
            tp_details = None
        else:
            tp_details = TakeProfitDetails(price=takeprofit_price).data
    
        if stoploss_price == 0:
            sl_details = None
        else:
            sl_details = StopLossDetails(price=stoploss_price).data
    
        mktOrder = MarketOrderRequest(
            instrument=instrument,
            units=units,
            takeProfitOnFill=tp_details,
            stopLossOnFill=sl_details
            )
        
        r = orders.OrderCreate(self.accountID, data=mktOrder.data)
        return self.request(r)

    
        
    def transactionDetails(self, transactionID):
        r = TransactionDetails(self.accountID, transactionID=transactionID)
        return self.request(r)

    def transactionsSinceID(self, transactionID):
        r = TransactionsSinceID(self.accountID, 
                                params={"id": transactionID})
        return self.request(r)

    
    
    def tradeDetails(self, tradeID):
        r = TradeDetails(self.accountID, tradeID=tradeID)
        return self.request(r)
    
    
    def trades(self, tradeID):
        r = TradesList(self.accountID, 
                       params={"tradeID": tradeID, "state": "ALL"})
        return self.request(r)
        


if __name__ == "__main__":
    oandaw = OandaWrapper()
    bid, ask = oandaw.getCurrPrice("USD_JPY")
    print("current rate bid=%f ask=%f" % (bid, ask))
    
    #req,res = oandaw.orderCreate("test1", "USD_JPY", "+1", ask+0.05, bid-0.05)
    #print("req=%s res=%s" % (req, res))
    
    r = oandaw.createMarketOrder("USD_JPY", 1, 
                    ask+0.05, bid-0.05)
    print(r)
    
    order_id = r["orderCreateTransaction"]["id"]
    
    
    #rv = oandaw.listOrders("test1")
    #print(rv)
    
    #rv = oandaw.listTrades("test1")
    #print(rv)
    
    rv = oandaw.transactionsSinceID(15)
    print(rv)
    

    