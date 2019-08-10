'''
Created on 2019/08/09

@author: kot
'''
from portfolio import Portfolio
import lib.names as names
import lib.sqllib as sqllib
from db.mssql import MSSQLDB
from tools.eventqueue import EventQueue
from event.trade import TradeEvent
from event.order import OrderEvent
import env

class MSSQLPortfolio(Portfolio):
    def getOrderHistoryEventQueue(self, startep=-1, endep=-1):
        db = MSSQLDB()
        orderhT = names.getOrderHistoryTable(self.transaction_name)
        orderh = EventQueue()
        self.orderhT = names.getOrderHistoryTable(self.transaction_name)
        sql = "select id, order_id, startep, validep, instrument, side, \
        order_type, units, price, takeprofit_price, stoploss_price, [desc] \
        from %s" % orderhT
        wherelist = []
        if startep > 0:
            wherelist.append("startep >= %d" % startep)
        if endep > 0:
            wherelist.append("endep <= %d" % endep)
        wherestr = sqllib.getWhereFromList(wherelist)
        sql += wherestr + ";"
        
        for (_id, order_id, startep, validep, instrument, side, \
        order_type, units, price, takeprofit_price, stoploss_price, desc) \
        in db.execute(sql):
            event = OrderEvent(_id, order_id, 
                instrument, side, order_type, units, price, 
                startep, status=env.ESTATUS_ORDER_CLOSED, 
                takeprofit_price=takeprofit_price, 
                stoploss_price=stoploss_price,
                validep=-1, endep=endep, desc="")
            orderh.append(_id, event)
        return orderh
        
        

    def getTradeHistoryEventQueue(self, startep=-1, endep=-1):
        db = MSSQLDB()
        tradeh = EventQueue()
        tradehT = names.getTradeHistoryTable(self.transaction_name)
        sql = "select id, trade_id, startep, endep,  \
        instrument, side, units, start_price, end_price, profit, \
        takeprofit_price, stoploss_price, [desc] from %s " % (tradehT)
        wherelist = []
        if startep > 0:
            wherelist.append("startep >= %d" % startep)
        if endep > 0:
            wherelist.append("endep <= %d" % endep)
        wherestr = sqllib.getWhereFromList(wherelist)
        sql += wherestr + ";"
        
        
        for (_id, trade_id, startep, endep, \
        instrument, side, units, start_price, end_price, profit, \
        takeprofit_price, stoploss_price, desc) in db.execute(sql):
            event = TradeEvent(_id, trade_id, 
                instrument, side, units, start_price, startep, 
                env.ESTATUS_TRADE_CLOSED, takeprofit_price, stoploss_price,
                end_price, profit, endep, desc)
            tradeh.append(_id, event)
        return tradeh
    
    
    def getPlotElement(self, startep=-1, endep=-1):
        pass
    
    def runSumSQL(self, selgroup1, selgroup2, grpbygroup, startep=-1, endep=-1):
        db = MSSQLDB()
        tablename = names.getTradeHistoryTable(self.transaction_name)
        wherelist = []
        if startep > 0:
            wherelist.append("startep >= %d" % startep)
        if endep > 0:
            wherelist.append("endep <= %d" % endep)
        wherestr = sqllib.getWhereFromList(wherelist)
        
        sql = "select %s, \
        profit, total, wins, loses, max_profit, max_lose, \
        wins*100/total as win_rate from \
        (select %s, \
        sum(profit) as profit, count(profit) as total, \
        sum(case when profit >= 0 then 1 else  0 end) as wins, \
        sum(case when profit < 0 then 1 else 0 end) as loses, \
        max(profit) as max_profit, min(profit) as max_lose \
          FROM %s %s group by %s) as p \
          order by %s;" % \
          (selgroup1, selgroup2, tablename, wherestr, grpbygroup, selgroup1)
        
        return db.get_df(sql)
    
    def getDailySum(self, startep=-1, endep=-1):
        return self.runSumSQL("y, m, d",
            "year(startdt) as y, month(startdt) as m, day(startdt) as d", 
                              "year(startdt), month(startdt), day(startdt)", 
                              startep, endep)
        
        
    def getMonthlySum(self, startep=-1, endep=-1):
        return self.runSumSQL("y, m",
            "year(startdt) as y, month(startdt) as m", 
                              "year(startdt), month(startdt)", 
                              startep, endep)
        
    def getYearlySum(self, startep=-1, endep=-1):
        return self.runSumSQL("y",
            "year(startdt) as y", 
                              "year(startdt)", 
                              startep, endep)
        
if __name__ == "__main__":
    po = MSSQLPortfolio("DensBreakBacktest")
    #print(po.getDailySum())
    print(po.getMonthlySum())
    print("finished")
    