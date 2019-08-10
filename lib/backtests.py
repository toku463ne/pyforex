'''
Created on 2019/04/22

@author: kot
'''
import lib.tradelib as tradelib
import env
import lib

def runDefaultBacktest(transaction_name, instrument, 
                       startep, endep, strategy, tick_period="M5"):
    from ticker.backtest import BackTestTicker
    from executor.backtester import BacktestExecutor
    from trading import Trading
    from transaction.mssql import MSSQLTransaction
    
    ticker = BackTestTicker(instrument, tick_period, 
                            startep, endep, spread=tradelib.getSpread(instrument))
    executor = BacktestExecutor()
    tran = MSSQLTransaction(transaction_name)
    trading = Trading()
    portofolio, plotelements = trading.run(ticker, executor, strategy, tran)
    return portofolio, plotelements


def runSimple(instrument, startstr, endstr, profitpips=5, tick_period="M1"):
    from strategy.simple import SimpleStrategy
    startep = lib.str2epoch(startstr, env.DATE_FORMAT_NORMAL)
    endep = lib.str2epoch(endstr, env.DATE_FORMAT_NORMAL)
    strategy = SimpleStrategy(instrument, profitpips=profitpips)
    return runDefaultBacktest("SimpleStgBacktest", instrument, 
                       startep, endep, strategy,tick_period=tick_period)
    
def runDensBreak(instrument, startstr, endstr):
    from strategy.densbreak import DensBreakStrategy
    startep = lib.str2epoch(startstr, env.DATE_FORMAT_NORMAL)
    endep = lib.str2epoch(endstr, env.DATE_FORMAT_NORMAL)
    
    strategy = DensBreakStrategy(instrument, startep, endep)
    return runDefaultBacktest("DensBreakBacktest", instrument, 
                       startep, endep, strategy)
    


#if __name__ == "__main__":
    #runSimple2("USD_JPY", "2019-04-02T09:00:00", "2019-04-02T18:00:00")
    #po, pe = runSlope2("USD_JPY", "H1", "2018-12-01T10:00:00", 
    #                  "2019-01-01T00:00:00")
    #print(po.getTotalProfit())
