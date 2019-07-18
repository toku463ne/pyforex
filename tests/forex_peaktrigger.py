'''
Created on 2019/04/27

@author: kot
'''
import unittest
from backtests import runPeakTrigger
import lib

class ForexPeakTriggerTest(unittest.TestCase):


    def testForexPeakTrigger(self):
        (oh, th) = runPeakTrigger("USD_JPY", "M5", 
                                  "2019-04-02T09:00:00", "2019-04-02T14:10:00")
        
        
        return
        ids = [1,2,3,4]
        sides = [-1,1,-1,1]
        self.assertTrue(lib.compWithEventQueue(oh, ids, sides, "side"), 
                        "order side check")
        
        prices = [111.392,111.340,111.390,111.343]
        self.assertTrue(lib.compWithEventQueue(oh, ids, prices, "price", ".3f"), 
                        "order price check")
        
        date_format = "%Y-%m-%dT%H:%M"
        timestrs = ["09:01","09:33","13:56","14:07"]
        timestrs = lib.addPrefix2List("2019-04-02T", timestrs)
        self.assertTrue(lib.compDateWithEventQueue(oh, ids, timestrs, 
                        "start_time", date_format), "start_time check")
        
        
        ids = [1,2,3]
        sides = [-1,1,-1]
        self.assertTrue(lib.compWithEventQueue(th, ids, sides, "side"), 
                        "trade side check")
        
        prices = [111.339,111.390,111.338]
        self.assertTrue(lib.compWithEventQueue(th, ids, prices, "end_price", ".3f"), 
                        "trade end_price check")
        
        profits = [0.052,0.050,0.052]
        self.assertTrue(lib.compWithEventQueue(th, ids, profits, "profit", ".3f"), 
                        "trade profit check")
        
        timestrs = ["09:32","13:55","14:06"]
        timestrs = lib.addPrefix2List("2019-04-02T", timestrs)
        self.assertTrue(lib.compDateWithEventQueue(th, ids, timestrs, 
                        "end_time", date_format), 
                        "trade end_time check")
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()