from event import *

'''
http://developer.oanda.com/rest-live-v20/order-df/#OrderRequest
'''
import pandas as pd

class Trader(object):
    def __init__(self):
        self.order_df = self._genOrderDF()
        self.trade_df = {}
        self.max_order_id = 0
        self.max_trade_id = 0
        
    def genOrderID(self):
        self.max_order_id += 1
        return self.max_order_id
    
    def genTradeID(self):
        self.max_trade_id += 1
        return self.max_trade_id
    
    
    def createOrderEvent(self, ep, valid_until, instrument, side, order_type, units, 
                 price, takeprofit_price=0, stoploss_price=0):
        local_order_id = self.genOrderID()
        self.order_df.loc[-1] = [local_order_id, -1, -1, ep, valid_until, 
                      instrument, side, order_type, units, 
                      price, takeprofit_price, stoploss_price]
        
        return order.OrderEvent(ep, instrument, side, order_type, units, 
                 price, takeprofit_price, stoploss_price)
        

    def _genOrderDF(self):
        df = pd.DataFrame(columns=["local_order_id", "order_id", "trade_id",
                                   "ordered_ep", "valid_until", 
                                   "instrument", "side", "order_type", "units", 
                                   "price", "takeprofit_price", "stoploss_price"])
        return df
        
        
        
        