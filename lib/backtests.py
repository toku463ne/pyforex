'''
Created on 2019/04/22

@author: kot
'''
import lib.tradelib as tradelib
import env
import lib

def runTestingBacktest(name, instrument, 
                       startep, endep, strategy, tick_period="M1"):
    from ticker.backtest import BackTestTicker
    from executor import Executor
    import trading
    from trademanager import TradeManager
    
    ticker = BackTestTicker(instrument, tick_period, 
                            startep, endep, 
                            spread=tradelib.getSpread(instrument))
    executor = Executor()
    manager = TradeManager(name)
    return trading.run(ticker, executor, strategy, manager, False)
    


#if __name__ == "__main__":
    #runSimple2("USD_JPY", "2019-04-02T09:00:00", "2019-04-02T18:00:00")
    #po, pe = runSlope2("USD_JPY", "H1", "2018-12-01T10:00:00", 
    #                  "2019-01-01T00:00:00")
    #print(po.getTotalProfit())
