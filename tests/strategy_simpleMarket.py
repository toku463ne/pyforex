'''
Created on 2019/11/16

@author: kot
'''
import unittest
import lib.testdata as testdata
from lib.backtests import runTestingBacktest
from strategy.simpleMarket import SimpleMarketStrategy
import lib

class TestSimpleMarketStrategy(unittest.TestCase):


    def testCase1(self):
        
        instrument = "USD_JPY"
        granularity = "M1"
        st = lib.str2epoch("2019-11-15T00:00:00")
        ed = lib.str2epoch("2019-11-15T01:00:00")
        testdata.prepare2legData(instrument, granularity, 
                                 100.0, st, ed)
        
        strategy = SimpleMarketStrategy(instrument, 10)
        history = runTestingBacktest("TestSimpleMarketStrategy", instrument, 
                       st, ed, strategy, tick_period=granularity)
        print(history)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()