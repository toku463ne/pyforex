'''
Created on 2019/05/01

@author: kot
'''
from collections import OrderedDict

class IndexedDict(object):
    def __init__(self, _id):
        self.id = _id   
        self.keys = []
        self.idxs = {}
        self.vals = {}
        
    def shiftKeys(self, nshift):
        tmp1 = {}
        for key in self.idxs:
            if key-nshift >= 0:
                tmp1[key-nshift] = self.idxs[key]
        self.idxs = tmp1
        tmp2 = {}
        for key in self.vals:
            if key-nshift >= 0:
                tmp2[key-nshift] = self.vals[key]
        self.vals = tmp2
        tmp3 = []
        for key in self.keys:
            if key-nshift >= 0:
                tmp3.append(key-nshift)
        self.keys = tmp3
        
            
            
    def __len__(self):
        return len(self.keys)
        
    def append(self, key, val):
        if key in self.idxs.keys():
            return
        self.keys.append(key)
        self.idxs[key] = len(self.keys)-1
        self.vals[key] = val
        
    def getKey(self, idx):
        return self.keys[idx]
    
    def hasKey(self, key):
        return key in self.keys
    
    def getIdx(self, key):
        return self.idxs[key]
    
    def get(self, key):
        return self.vals[key]
    
    def popitem(self, last=True):
        if last:
            retk = self.keys.pop()
            retv = self.vals[retk]
        else:
            retk = self.getKey(0)
            retv = self.vals[retk]
            del self.keys[0]
        del self.idxs[retk]
        del self.vals[retk]
        return retk, retv
    
    def getData(self):
        od = OrderedDict()
        for key in self.keys:
            od[key] = self.vals[key]
        return od
        
        
    def __iter__(self):
        for k in self.keys:
            yield self.vals[k]