'''
Created on 2019/04/15

@author: kot
'''
from executor import Executor
import env
from event.trade import TradeEvent
import lib

class BacktestExecutor(Executor):
    def checkOrder(self, ep, event, bid, ask):
        if event.side == env.SIDE_BUY:
            price = ask
        else:
            price = bid
        if event.order_type == env.ORDER_MARKET:
            lib.printInfo(ep, "orderC id=%d" % (event.id))
            trade_event = TradeEvent(event.id, -1, 
                event.instrument, event.side, event.units, price, ep, 
                takeprofit_price=event.takeprofit_price,
                stoploss_price=event.stoploss_price,
                desc=event.desc)
            event.status = env.ESTATUS_ORDER_CLOSED
            self.tran.trade_queue.appendleft(event.id, trade_event)
            
            
    def checkTrade(self, ep, event, bid, ask):
        if event.side == env.SIDE_BUY:
            price = bid
        else:
            price = ask
        side = event.side
        trade_closed = False
        if event.status == env.ESTATUS_TRADE_CLOSE_REQUESTED:
            trade_closed = True
        elif event.status == env.ESTATUS_TRADE_ONGOING:
            if event.stoploss_price > 0:
                if price*side < event.stoploss_price*side:         
                    trade_closed = True
            if event.takeprofit_price > 0:
                if price*side > event.takeprofit_price*side:         
                    trade_closed = True
        
        if trade_closed:
            event.end_price = price
            event.end_time = ep
            event.profit = (event.end_price - event.start_price) * event.units * event.side
            event.status = env.ESTATUS_TRADE_CLOSED
        
        