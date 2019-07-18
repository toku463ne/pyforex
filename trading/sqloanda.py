'''
Created on 2019/04/13

@author: kot
'''
from trading import Trading
from ticker.backtest import BackTestTicker
from data_getter import MSSQLGetter
from data_getter import OandaGetter
from data_getter import DataGetter

class SqlOandaTrading(Trading):
    
    def runBacktestOffline(self, instrument, granularity, startep, endep):
        dg = DataGetter(MSSQLGetter(OandaGetter(instrument, granularity)))
        ti = BackTestTicker(dg, startep, endep)
        self._run(ti)
    