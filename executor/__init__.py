import env
import lib
from event.trade import TradeEvent
from event.signal import SignalEvent

class Executor(object):
    def issueOrder(self, event):
        pass
    
    def checkOrder(self, ep, order_event, bid=0, ask=0):
        pass
    
    def checkTrade(self, ep, trade_event, bid=0, ask=0):
        pass
    
    def _run(self, event):
        if event.type == env.EVETYPE_ORDER:
            self.issueOrder(event)
        if event.type == env.EVETYPE_TICK:
            self._checkOrders(event)
            self._checkTrades(event)
    
    def createTrade(self, ep, trade_id, order_event):
        oe = order_event
        event = TradeEvent(oe.id, trade_id, oe.instrument, oe.side, oe.units,
                           oe.price, ep, takeprofit_price=oe.takeprofit_price, 
                           stoploss_price=oe.stoploss_price, desc=oe.desc)
        self.tran.trade_queue.appendleft(oe.id, event)
        lib.printInfo(ep, "tradeO id=%d %.3f" % (oe.id, oe.price))
         
    
    
    def _checkOrders(self, event):
        ep = event.time
        bid = event.bid
        ask = event.ask
        quelen = len(self.tran.order_queue)
        for _ in range(quelen):
            _id, order_event = self.tran.order_queue.pop()
            self.checkOrder(ep, order_event, bid, ask)
            if order_event.status >= env.ESTATUS_ORDER_CLOSED:
                self.tran.order_hqueue.append(_id, order_event)
            else:
                self.tran.order_queue.appendleft(_id, order_event)
            
            
    def _checkTrades(self, event):
        ep = event.time
        bid = event.bid
        ask = event.ask
        quelen = len(self.tran.trade_queue)
        for _ in range(quelen):
            _id, trade_event = self.tran.trade_queue.pop()
            if trade_event.status == env.ESTATUS_TRADE_OPENED:
                trade_event.status = env.ESTATUS_TRADE_ONGOING
                self.tran.trade_queue.appendleft(_id, trade_event)
                lib.printInfo(ep, "tradeO id=%d %.3f" % (_id, trade_event.start_price))
                continue
            self.checkTrade(ep, trade_event, bid, ask)
            
            if trade_event.status >= env.ESTATUS_TRADE_CLOSED:
                lib.printInfo(trade_event.end_time, "tradeC id=%d %.3f profit=%.3f" % \
                              (trade_event.id, trade_event.end_price, 
                               trade_event.profit))
                signal_event = SignalEvent(_id, env.ESIGNAL_TRADE_CLOSED)
                signal_event.trade_event = trade_event
                self.queue.appendleft(signal_event)
                self.tran.trade_hqueue.append(_id, trade_event)
            else:
                self.tran.trade_queue.appendleft(_id, trade_event)
            
            