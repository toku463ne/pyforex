from tools.eventqueue import EventQueue


class Transaction(object):
    def __init__(self, name):
        self.name = name
        self.order_hqueue = EventQueue()
        self.trade_hqueue = EventQueue()
        self.order_queue = EventQueue()
        self.trade_queue = EventQueue()
        
        
    # return sequencial ID
    def genID(self):
        pass
    
    def getPortofolio(self):
        pass
    
    def flushOrderHistory(self):
        pass
    
    def flushTradeHistory(self):
        pass
    
    def flush(self):
        self.flushOrderHistory()
        self.flushTradeHistory()
    
    def addOrder(self, _id, event):
        self.order_queue.appendleft(_id, event)
        
    def popOrder(self):
        _id, order_event = self.order_queue.pop()
        return _id, order_event
    
    def addOrderHistory(self, _id, event):
        self.order_hqueue.appendleft(_id, event)
    
    def addTrade(self, _id, event):
        self.trade_queue.appendleft(_id, event)
    
    def popTrade(self):
        _id, trade_event = self.trade_queue.pop()
        return _id, trade_event
    
    def getTrade(self, _id):
        event = self.trade_queue.getAt(_id)
        return event
    
    def addTradeHistory(self, _id, event):
        self.trade_hqueue.appendleft(_id, event)
    
    