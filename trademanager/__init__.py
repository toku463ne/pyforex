
import env
import lib
import copy

class TradeManager(object):
    def __init__(self, name):
        self.name = name
        self.maxID = 0
        self.orders = {}
        self.transactions = []
        self.history = []
        
    def genID(self):
        self.maxID += 1
        return self.maxID
    
    def IDExists(self, _id):
        if _id in self.orders.keys():
            return True
        else:
            return False
        
    def openOrder(self, orderEvent):
        _id = orderEvent.id
        if not _id in self.orders.keys():
            self.orders[_id] = orderEvent
            lib.log("[%s] %s Order %d opened. %f side=%d tp=%f sl=%f" % (
                        self.name,
                        lib.epoch2str(orderEvent.epoch),
                        _id, 
                        orderEvent.price, orderEvent.side,
                        orderEvent.takeprofit_price, 
                        orderEvent.stoploss_price))
        else:
            raise Exception("Order %d already open." % _id)
    
    def closeOrder(self, orderEvent, epoch):
        _id = orderEvent.id
        if _id in self.orders.keys():
            self.history.append(self.orders[_id])
            del self.orders[_id]
            lib.log("[%s] %s Order %d closed. %f side=%d profit=%f %s" % (
                        self.name,
                        lib.epoch2str(epoch),
                        _id, 
                        orderEvent.trade_end_price, 
                        orderEvent.side, orderEvent.trade_profit, 
                        orderEvent.desc))
    
    def flushHistory(self):
        self.history = []
      
    def getOrder(self, _id):
        if _id in self.orders.keys():
            return self.orders[_id]
        else:
            return None
    
    def getOrders(self):
        return copy.deepcopy(self.orders)
    
    def updateOrder(self, orderEvent):
        _id = orderEvent.id
        if _id in self.orders.keys():
            self.orders[_id] = orderEvent
    
    def appendTransaction(self, orderEvent):
        return self.transactions.append(orderEvent)
            
    def popTransaction(self):
        return self.transactions.pop(0)
    
    