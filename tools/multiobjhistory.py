'''
Created on 2019/11/26

@author: kot
'''
from collections import OrderedDict

class MultiObjHistory(object):
    def __init__(self, size):
        self.history = OrderedDict()
        self.size = size
        
    def append(self, epoch, obj):
        if epoch not in self.history.keys():
            self.history[epoch] = []
        self.history[epoch].append(obj)
        
        if len(self.history.keys()) > self.size:
            oldepoch = self.history.keys()[0]
            del self.history[oldepoch]
    
    def last(self):
        epoch = self.history.keys()[-1]
        return epoch, self.history[epoch]
    