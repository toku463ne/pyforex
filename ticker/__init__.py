
import env

class Ticker(object):
    def __init__(self, dataGetter):
        self.dataGetter = dataGetter
        self.ticker_type = env.TICKTYPE_OFFLINE
    
    
    def tick(self):
        pass