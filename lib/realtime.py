'''
Created on 2019/08/10

@author: kot
'''

def runDefaultCandleTrading(transaction_name, instrument, 
                            strategy, localTrading=False):
    from ticker.latestoandacandle import LastOandaCandleTicker
    from trading import Trading
    from transaction.mssql import MSSQLTransaction
    if localTrading:
        from executor.backtester import BacktestExecutor
        executor = BacktestExecutor()
    else:
        from executor.oandamssql import OandaMSSQLExecutor
        executor = OandaMSSQLExecutor(transaction_name)
    ticker = LastOandaCandleTicker(instrument)
    tran = MSSQLTransaction(transaction_name)
    trading = Trading()
    portofolio, plotelements = trading.run(ticker, executor, strategy, tran)
    return portofolio, plotelements


def runSimple(instrument="USD_JPY", 
               profitpips=3, localTrading=False):
    from strategy.simple import SimpleStrategy
    strategy = SimpleStrategy(instrument, profitpips)
    return runDefaultCandleTrading("Simple2Strategy", instrument, 
                       strategy, localTrading)
    

def runSimple2(instrument="USD_JPY", granularity="H1", 
               profitpips=5, localTrading=False):
    from strategy.simple2 import Simple2Strategy
    strategy = Simple2Strategy(instrument, granularity, profitpips)
    return runDefaultCandleTrading("Simple2Strategy", instrument, 
                       strategy, localTrading)
    
    
