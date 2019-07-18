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
    def __init__(self):
        self.oandaw = OandaWrapper()
    
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
            event.trade_id = data["tradeID"]
            event.first_tran_id = res["relatedTransactionIDs"][-1]
        
        
    def checkOrder(self, ep, event, _, _):
        event.status = env.ESTATUS_ORDER_CLOSED    
    
    
    