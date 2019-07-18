'''
Created on 2019/04/15

@author: kot
'''
from event.eventqueue import EventQueue

class Transaction(object):
    def __init__(self):
        self.order_hqueue = EventQueue()
        self.trade_hqueue = EventQueue()
        self.order_queue = EventQueue()
        self.trade_queue = EventQueue()
        self.max_id = 0
        

    
