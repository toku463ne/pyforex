
import pandas as pd
import lib

class EventQueue(object):
    def __init__(self):
        self.dict = {}
        self.list = []
        
    def appendleft(self, _id, obj):
        if _id in self.dict.keys():
            return False
        self.list.insert(0, _id)
        self.dict[_id] = obj
        return True
    
    def __len__(self):
        return len(self.list)
    
    def append(self, _id, obj):
        self.list.append(_id)
        self.dict[_id] = obj
        return True
    
    def getLast(self):
        if len(self.list) == 0:
            return (-1, None)
        _id = self.list[-1]
        obj = self.dict[_id]
        return (_id, obj)
    
    def getFirst(self):
        _id = self.list[0]
        obj = self.dict[_id]
        return (_id, obj)
    
    def getAt(self, _id):
        if _id in self.dict.keys():
            return self.dict[_id]
        else:
            return None
    
    def pop(self):
        if len(self.list) == 0:
            return (-1, None)
        _id = self.list.pop()
        obj = self.dict[_id]
        del self.dict[_id]
        return (_id, obj)
    
    def getDataFrame(self):
        if len(self.list) == 0:
            return pd.DataFrame()
        sample = self.dict[self.list[0]]
        df = pd.DataFrame(columns=sample.__dict__.keys(), index=self.list)
        for _id in self.list:
            ev = self.dict[_id]
            for col in sample.__dict__.keys():
                val = ev.__dict__[col]
                if col == "start_time" or col == "end_time":
                    val = lib.epoch2dt(val)
                df.loc[_id][col] = val
                
        return df
    
    
    