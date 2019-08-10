'''
Created on 2019/05/03

@author: kot
'''

from executor import Executor
from event.trade import TradeEvent
from tools.oanda import OandaWrapper
import env
import lib


class OandaExecutor(Executor):
    class IDMap():
        def __init__(self, orderID, tradeID=-1):
            self.orderID = orderID
            self.tradeID = tradeID
    
    def __init__(self):
        self.oandaw = OandaWrapper()
        self.idmaps = {}
    
    
    def issueOrder(self, event):
        if event.order_type == env.ORDER_MARKET:
            res = self.oandaw.createMarketOrder(event.instrument, 
                                event.units*event.side,
                                event.takeprofit_price, 
                                event.stoploss_price)
            lib.printInfo(lib.nowepoch(), 
                          "Issued market order: %s units=%d tp=%f sl=%f\n%s" % (
                              event.instrument, event.units*event.side,
                              event.takeprofit_price, event.stoploss_price,
                              res))
            data = res["orderCreateTransaction"]
            event.order_id = data["id"]
    
    # Do nothing here
    def checkOrder(self, ep, order_event, bid=0, ask=0):
        pass
    
    
    
    def checkTrade(self, ep, trade_event, bid=0, ask=0):
        pass
       
    
    
    