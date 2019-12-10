'''
Created on 2019/11/26

@author: kot
'''
from collections import OrderedDict
import lib

class MultiObjHistory(object):
    def __init__(self):
        self.history = OrderedDict()
        
    def append(self, epoch, obj, epoch_to_remove_old=0):
        if epoch not in self.history.keys():
            self.history[epoch] = []
        self.history[epoch].append(obj)
        
        if epoch_to_remove_old > 0:
            for epoch in  list(self.history.keys()):
                if epoch >= epoch_to_remove_old:
                    break
                del self.history[epoch]
    
    def __getitem__(self, epoch):
        if epoch in self.history.keys():
            return self.history[epoch]
        else:
            return None
    
    def __iter__(self):
        for (k,obj) in self.history.items():
            yield k,obj
        
    def __len__(self):
        return len(self.history)
    
    def last(self):
        epoch = self.history.keys()[-1]
        return epoch, self.history[epoch]
    