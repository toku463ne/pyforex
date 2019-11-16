'''
Created on 2019/05/03

@author: kot
'''

from executor.backtester import BacktestExecutor
from tools.oanda import OandaWrapper
from db.mssql import MSSQLDB
import lib.names as names
import lib.sqllib as sqllib

import env
import lib


class OandaMSSQLExecutor(BacktestExecutor):
    
    def __init__(self, transaction_name):
        self.oandaw = OandaWrapper()
        self.transaction_name = transaction_name
        self.last_transaction_id = self.getLastTransactionID()
        self.processing_ids = []
    
        
    def getLastTransactionID(self):
        db = MSSQLDB()
        tname = names.getOandaTrandactionIDTableName()
        db.createTable(tname, "oanda_transaction_id")
        sql = "select last_transaction_id from %s " % tname
        oconf = env.conf["oanda"]
        wherelist = ["transaction_name = '%s'" % self.transaction_name,
                     "environment = '%s'" % oconf["environment"],
                     "account_id = '%s'" % oconf["accountid"]
                      ]
        wherestr = sqllib.getWhereFromList(wherelist)
        sql += wherestr
        last_transaction_id = 1
        for tid in db.execute(sql):
            last_transaction_id = tid
        return last_transaction_id
    
    
    def issueOrder(self, event):
        if event.order_type == env.ORDER_MARKET:
            res = self.oandaw.createMarketOrder(event.instrument, 
                                event.units*event.side,
                                event.takeprofit_price, 
                                event.stoploss_price)
            data = res["orderCreateTransaction"]
            event.order_id = data["id"]
            lib.printInfo(lib.nowepoch(), 
                          "[oanda] MarketOrder: orderID=%s %s units=%d tp=%f sl=%f\n%s" % (
                              event.order_id, 
                              event.instrument, event.units*event.side,
                              event.takeprofit_price, event.stoploss_price,
                              res))
            
    
    def checkOrder(self, ep, order_event, bid=-1, ask=-1):
        '''
        check transactions
        type=ORDER_FILL
        orderID
        instrument
          get tradeID from "tradeOpened"
        '''
        rv = self.oandaw.transactionsSinceID(self.last_transaction_id)
        orderID = order_event.order_id
        for tran in rv["transactions"]:
            if tran["type"] == "ORDER_FILL" and \
            tran["orderID"] == orderID:
                if not "tradeOpened" in tran.keys():
                    return
                trade = tran["tradeOpened"]
                super(OandaMSSQLExecutor, self).checkOrder(ep, 
                                        order_event, trade["price"],
                                        trade["price"],
                                        trade["tradeID"])
                self.processing_ids.append(tran["id"])
                self.last_transaction_id = min(self.processing_ids)
                break
    
    
    def checkTrade(self, ep, trade_event, bid=0, ask=0):
        rv = self.oandaw.transactionsSinceID(self.last_transaction_id)
        tradeID = trade_event.trade_id
        for tran in rv["transactions"]:
            if tran["type"] == "ORDER_FILL" and \
                "tradesClosed" in tran.keys():
                trades = tran["tradesClosed"]
                for trade in trades:
                    if trade["tradeID"] == tradeID:
                        trade_event.end_price = trade["price"]
                        trade_event.endep = ep
                        trade_event.profit = trade["realizedPL"]
                        trade_event.status = env.ESTATUS_TRADE_CLOSED
                        
                        lib.printInfo(lib.nowepoch(), 
                            "[oanda] tradeClose: tradeID=%s" % \
                            tradeID)
            
                        break
                break
    