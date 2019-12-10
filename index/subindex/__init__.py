
class SubIndex(object):
    def __init__(self, subChart):
        self.subChart = subChart
        self.now = subChart.getNow()
    
    def calc(self, epoch, **keys):
        pass
    
    def deleteOldProc(self, epoch, **keys):
        pass
    
    def getPlotElements(self, color="k"):
        return []