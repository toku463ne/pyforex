'''
Created on 2019/11/16

@author: kot
'''
import unittest
import lib.testdata as testdata
from lib.backtests import runTestingBacktest
from strategy.simpleStop import SimpleStopStrategy
import lib

class TestSimpleStopStrategy(unittest.TestCase):


    def testCase1(self):
        
        instrument = "USD_JPY"
        granularity = "M5"
        st = lib.str2epoch("2019-11-15T00:00:00")
        ed = lib.str2epoch("2019-11-15T01:00:00")
        testdata.prepare2legData(instrument, granularity, 
                                 100.0, st, ed, 3)
        testdata.makeSmallPeriodData(instrument, granularity, "M1")
        
        strategy = SimpleStopStrategy(instrument, granularity, 5)
        history = runTestingBacktest("c2", instrument, 
                       st, ed, strategy)
        
        res = history[0]
        self.assertEqual(res.id, 1, "id")
        self.assertEqual(res.epoch, 
                         lib.str2epoch("2019-11-15T00:02:00"), "order start")
        self.assertEqual(res.trade_open_time, 
                         lib.str2epoch("2019-11-15T00:04:00"), "trade start")
        self.assertEqual(res.trade_close_time, 
                         lib.str2epoch("2019-11-15T00:10:00"), "trade close")
        self.assertEqual(res.trade_profit, 0.047, "profit")
        
        res = history[1]
        self.assertEqual(res.id, 2, "id")
        self.assertEqual(res.epoch, 
                         lib.str2epoch("2019-11-15T00:11:00"), "order start")
        self.assertEqual(res.order_close_time, 
                         lib.str2epoch("2019-11-15T00:16:00"), "order close")
        
        res = history[5]
        self.assertEqual(res.id, 6, "id")
        self.assertEqual(res.epoch, 
                         lib.str2epoch("2019-11-15T00:46:00"), "order start")
        self.assertEqual(res.trade_close_time, 
                         lib.str2epoch("2019-11-15T00:59:00"), "trade close")
        #print(history)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()