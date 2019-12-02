'''
Created on 2019/11/30

@author: kot
'''

import lib
from strategy.priceAction import PriceActionStrategy
from lib.backtests import runTestingBacktest
import env

env.run_mode = env.MODE_BACKTESTING
env.loglevel = env.LOGLEVEL_DEBUG

instrument = "USD_JPY"
granularity = "M5"
st = lib.str2epoch("2019-11-28T00:00:00")
ed = lib.str2epoch("2019-11-29T00:00:00")
strategy = PriceActionStrategy(instrument, granularity, st, ed)
history = runTestingBacktest("experiment", instrument, 
               st, ed, strategy)
print("Finish")

