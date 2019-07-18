'''
Created on 2019/05/01

@author: kot
'''
import unittest
import lib.tradelib as tradelib
import lib
import env

class TestIndexPeaks(unittest.TestCase):


    def testIndexPeaks1(self):
        from strategy.peaktester import PeakTesterStrategy
        
        instrument = "USD_JPY"
        granularity = "M5"
        startstr = "2019-04-02T09:00:00"
        endstr = "2019-04-02T11:30:00"
        startep = lib.str2epoch(startstr, env.DATE_FORMAT_NORMAL)
        endep = lib.str2epoch(endstr, env.DATE_FORMAT_NORMAL)
        nbars = 15
        peak_span = 3
        cachesize = 5
        maxsize = 100
        strategy = PeakTesterStrategy(instrument, granularity, startep, endep, nbars, 
                 peak_span, cachesize, maxsize)
        tradelib.runDefaultBacktest(instrument, startep, endep, strategy)
        peak = strategy.peak
        ma = peak.maxpeaks
        prices = [111.402,111.381,111.373]
        self.assertTrue(lib.compFloatList(list(ma.vals.values()), 
                                          prices, "%.3f"), "max_peaks")
        
        mi = peak.minpeaks
        prices = [111.344,111.310,111.322,111.323]
        self.assertTrue(lib.compFloatList(list(mi.vals.values()), 
                                          prices, "%.3f"), "min_peaks")
        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()