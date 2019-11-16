import env
import lib
from event.signal import SignalEvent

class Executor(object):
    # self.manager is set on trading.Trading
    
    def receiveOrder(self, orderEvent):
        self.manager.appendTransaction(orderEvent)
    
      
    # return list of signal_events
    def onTick(self, tickEvent):
        signal_events = []
        
        # operate existing orders
        orders = self.manager.getOrders()
        for _id in orders.keys():
            orderEvent = orders[_id]
            self.checkOrder(tickEvent, orderEvent)
            if orderEvent.status in [env.ESTATUS_ORDER_CLOSED,
                                     env.ESTATUS_TRADE_OPENED,
                                     env.ESTATUS_TRADE_CLOSED]:
                signal_events.append(SignalEvent(_id, 
                                        orderEvent.status))
            if orderEvent.status in [env.ESTATUS_ORDER_CLOSED,
                                 env.ESTATUS_TRADE_CLOSED]:
                self.manager.closeOrder(orderEvent, tickEvent.time)
                
            
            
        # operate new orders
        while len(self.manager.transactions) > 0:
            orderEvent = self.manager.popTransaction()
            _id = orderEvent.id
            orgEvent = self.manager.getOrder(_id)
            
            if orderEvent.cmd == env.CMD_CANCEL:
                self.cancelOrder(tickEvent, orgEvent)
                self.manager.closeOrder(orgEvent, tickEvent.time)
                signal_events.append(SignalEvent(_id, 
                                        orgEvent.status))
                continue
            
            if orgEvent != None:
                raise Exception("id=%d already exists!" % _id)
            
            if orderEvent.cmd in [env.CMD_CREATE_STOP_ORDER,
                             env.CMD_CREATE_LIMIT_ORDER,
                             env.CMD_CREATE_MARKET_ORDER]:
                self.issueOrder(tickEvent, orderEvent)
                self.manager.openOrder(orderEvent)
                signal_events.append(SignalEvent(_id, orderEvent.status))
    
        return signal_events
        
    # must override
    def issueOrder(self, tickEvent, orderEvent):
        orderEvent.status = env.ESTATUS_ORDER_OPENED
        self.manager.updateOrder(orderEvent)
    
    # must override
    def cancelOrder(self, tickEvent, orderEvent):
        if orderEvent.side == env.SIDE_BUY:
            price = tickEvent.bid
        else:
            price = tickEvent.ask
        
        if orderEvent.status == env.ESTATUS_ORDER_OPENED:
            orderEvent.close_order(tickEvent, "Order cancel")
        if orderEvent.status == env.ESTATUS_TRADE_OPENED:
            orderEvent.close_trade(tickEvent, price, "Trade cancel")
    
    # make sure to update orderEvent status accordingly
    def checkOrder(self, tickEvent, orderEvent):
        if orderEvent.side == env.SIDE_BUY:
            price = tickEvent.ask
        else:
            price = tickEvent.bid
        
        side = orderEvent.side
    
        
        if orderEvent.status == env.ESTATUS_ORDER_OPENED:
            if orderEvent.cmd == env.CMD_CREATE_MARKET_ORDER:
                orderEvent.start_trade(tickEvent, price, "Market order")
                self.manager.updateOrder(orderEvent)
                
            elif orderEvent.cmd == env.CMD_CREATE_STOP_ORDER:
                orderEvent.check_valid(tickEvent)
                if price*side < orderEvent.price*side:
                    orderEvent.start_trade(tickEvent, price, 
                                           "Stop order filled")
                    self.manager.updateOrder(orderEvent)
                    
            else:
                raise Exception("Non supported cmd")
        
        elif orderEvent.status == env.ESTATUS_TRADE_OPENED:
            tp = orderEvent.takeprofit_price
            sl = orderEvent.stoploss_price
            
            if price*side >= tp*side:
                orderEvent.close_trade(tickEvent, price, "takeprofit")
                self.manager.updateOrder(orderEvent)
            
            if price*side <= sl*side:
                orderEvent.close_trade(tickEvent, price, "stoploss")
                self.manager.updateOrder(orderEvent)
            
            