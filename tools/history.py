'''
Created on 2019/11/30

@author: kot
'''
from collections import OrderedDict

class History(object):
    def __init__(self, size, deleteOld=True):
        self.history = OrderedDict()
        self.size = size
        self.deleteOld = deleteOld
    
    def append(self, epoch, obj):
        self.history[epoch] = obj
        
        if self.deleteOld:
            if len(self.history) > self.size:
                del self.history[self.history.keys()[0]]
    
    def last(self):
        keys = list(self.history.keys())
        if len(keys) == 0:
            return -1, -1
        epoch = keys[-1]
        return epoch, self.history[epoch]
           