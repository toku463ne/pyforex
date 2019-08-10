
from event.order import OrderEvent
import env
import lib

class Strategy(object):
    
    def onTick(self, tickEvent):
        pass
    
    def onSignal(self, signalEvent):
        pass




    def _genID(self):
        return self.tran.genID()
            

    def _run(self, event):
        if event.type == env.EVETYPE_TICK:
            self.onTick(event)
        if event.type == env.EVETYPE_SIGNAL:
            self.onSignal(event)


    #_id, instrument, side, order_type, units, 
    #             price, takeprofit_price=0, stoploss_price=0, valid_time, desc
    def createOrder(self, ep, instrument, side, order_type, units, 
                 price, validep=0, takeprofit_price=0, stoploss_price=0, desc=""):
        _id = self._genID()
        event = OrderEvent(_id, -1, instrument, side, order_type, units, price, 
                ep, takeprofit_price=takeprofit_price, 
                stoploss_price=stoploss_price,
                validep=validep, desc=desc)
        self.tran.addOrder(_id, event)
        lib.printInfo(ep, "orderO id=%d %s s=%d type=%d u=%d %.3f \
t/p=%.3f s/l=%.3f vl=%d %s" % (_id, instrument,
                    side, order_type, units, price, takeprofit_price, 
                    stoploss_price,
                    validep, desc))
        return _id
        
        
    def closeTrade(self, _id):
        event = self.tran.getTrade(_id)
        if event != None:
            event.status = env.ESTATUS_TRADE_CLOSE_REQUESTED
          
    def getPlotElements(self, color="k"):
        return []