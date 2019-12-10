'''
Created on 2019/12/09

@author: kot
'''
from index.histindex import HistIndex
from tools.subchart import SubChart
import lib
from event.history import HistEvent
from event.tick import TickEvent

class TestHistIndex(HistIndex):

    def __init__(self):
        self.startep = lib.str2epoch("2019-11-27T17:45:00")
        self.endep = lib.str2epoch("2019-11-28T00:25:00")
        name = "TestHistIndex"
        subc = SubChart(name, "USD_JPY", "M5",
                        startep=self.startep, endep=self.endep)
        super(TestHistIndex, self).__init__("TestHistIndex", subc)
        super(HistIndex, self).__init__(name, subc)
        subc.onTick(TickEvent(self.endep,0,0,0))
        (t,_,_,_,_,_) = subc.getPrices(self.startep, self.endep)
        self.subc = subc
        for epoch in t:
            self.calcHist(epoch)
        
        
    def calcHistBasePrices(self, epoch):
        lines = [109.47, 109.55]
        #(_,_,h,_,_,_) = self.subc.getNPrices(epoch, 1)
        hes = []
        for line in lines:
            price = line 
            index_id = int(price * 100)
            index_type = 0
            he = HistEvent(epoch, price, 
                 index_id, index_type, color="r", marker="o")
            hes.append(he)
        return hes
    
    
    
def run():
    t = TestHistIndex()
    return (t.getPlotElements(),
        t.instrument, t.granularity, t.startep, t.endep)
    
if __name__ == "__main__":
    run()
    
            