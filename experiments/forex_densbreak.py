'''
Created on 2019/08/09

@author: kot
'''
from lib.backtests import runDensBreak
import env

env.run_mode = env.MODE_SIMULATE
po, _ = runDensBreak("USD_JPY", "2015-01-01T00:00:00", 
                             "2019-08-01T00:00:00")

print(po.getMonthlySum())
print(po.getYearlySum())
