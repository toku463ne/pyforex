'''
Created on 2019/04/27

@author: kot
'''
import unittest
from lib.backtests import runDensBreak
import lib
import lib.testing as testlib
import env

class ForexDensBreakTest(unittest.TestCase):
    def testCase1(self):
        print("Running in backtesting mode")
        env.run_mode = env.MODE_BACKTESTING
        self._case1()
        
        print("Running in simulation mode")
        env.run_mode = env.MODE_SIMULATE
        self._case1()

    def _case1(self):
        po, _ = runDensBreak("USD_JPY", "2019-04-01T00:00:00", 
                             "2019-04-11T00:00:00")
        oh = po.getOrderHistoryEventQueue()
        
        
        ids = [1,2,3,4]
        sides = [-1,1,-1,1]
        self.assertTrue(testlib.compWithEventQueue(oh, ids, sides, "side"), 
                        "order side check")
        
        prices = [111.392,111.340,111.390,111.343]
        self.assertTrue(testlib.compWithEventQueue(oh, ids, prices, "price", ".3f"), 
                        "order price check")
        
        date_format = "%Y-%m-%dT%H:%M"
        timestrs = ["09:01","09:33","13:56","14:07"]
        timestrs = lib.addPrefix2List("2019-04-02T", timestrs)
        self.assertTrue(testlib.compDateWithEventQueue(oh, ids, timestrs, 
                        "startep", date_format), "startep check")
        
        th = po.getTradeHistoryEventQueue()
        ids = [1,2,3]
        sides = [-1,1,-1]
        self.assertTrue(testlib.compWithEventQueue(th, ids, sides, "side"), 
                        "trade side check")
        
        prices = [111.339,111.390,111.338]
        self.assertTrue(testlib.compWithEventQueue(th, ids, prices, "end_price", ".3f"), 
                        "trade end_price check")
        
        profits = [0.052,0.050,0.052]
        self.assertTrue(testlib.compWithEventQueue(th, ids, profits, "profit", ".3f"), 
                        "trade profit check")
        
        timestrs = ["09:32","13:55","14:06"]
        timestrs = lib.addPrefix2List("2019-04-02T", timestrs)
        self.assertTrue(testlib.compDateWithEventQueue(th, ids, timestrs, 
                        "endep", date_format), 
                        "trade endep check")
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()