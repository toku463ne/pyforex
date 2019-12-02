'''
Created on 2019/11/16

@author: kot
'''
import unittest
import lib
from index.peaks import PeakIndex
from event.tick import TickEvent
from tools.subchart import SubChart

class TestPeakIndex(unittest.TestCase):


    def testCase1(self):
        
        instrument = "USD_JPY"
        granularity = "M5"
        startep = lib.str2epoch("2019-11-12T12:00:00")
        endep = lib.str2epoch("2019-11-12T15:00:00")
        peakspan = 48
        peaksize = 5
        subc = SubChart("PeakIndex%d" % peakspan, 
                             instrument, granularity, startep, 
                             endep, nbars=max(peakspan+peaksize*2+1,
                                              peakspan*2))
        
        p = PeakIndex(subc, peaksize, peakspan, peakspan*2)
        
        # Just after initialization
        self.assertEqual(len(p.tops), 4)
        self.assertEqual(len(p.bottoms), 6)
        
        self.assertEqual(p.tops[1573548300], 109.266)
        self.assertEqual(p.tops[1573553400], 109.205)
        
        self.assertEqual(p.bottoms[1573545600], 109.21)
        self.assertEqual(p.bottoms[1573558200], 109.184)
        
        self.assertEqual(len(p.top_trendlines), 2)
        self.assertEqual(len(p.bottom_trendlines), 1)
        
        self.assertEqual("%.8f" % p.top_trendlines[1573550700], '-0.00000593')
        self.assertEqual("%.8f" % p.top_trendlines[1573548300], '-0.00001196')
        self.assertEqual("%.8f" % p.bottom_trendlines[1573554300], '0.00000769')
        
        self.assertEqual("%.3f" % p.maxs[1573548300] , '109.266')
        self.assertEqual("%.3f" % p.mins[1573552500] , '109.142')
        
        #After tick
        epoch = startep + 60
        tickEvent = TickEvent(epoch, 0, 0, 0)
        subc.onTick(tickEvent)
        self.assertFalse(p.onTick(tickEvent))
        
        epoch = startep + 300
        tickEvent = TickEvent(epoch, 0, 0, 0)
        subc.onTick(tickEvent)
        self.assertTrue(p.onTick(tickEvent))
        
        
        epoch = lib.str2epoch("2019-11-12T14:00:00")
        tickEvent = TickEvent(epoch, 0, 0, 0)
        subc.onTick(tickEvent)
        self.assertTrue(p.onTick(tickEvent))
        
        self.assertEqual(len(p.tops), 5)
        self.assertEqual(len(p.bottoms), 6)
        self.assertEqual(len(p.top_trendlines), 1)
        self.assertEqual(len(p.bottom_trendlines), 3)
        
        
        
        self.assertEqual(p.tops[1573553100], 109.205)
        self.assertEqual(p.bottoms[1573552500], 109.142)
        
        epoch = lib.str2epoch("2019-11-12T16:00:00")
        tickEvent = TickEvent(epoch, 0, 0, 0)
        subc.onTick(tickEvent)
        self.assertTrue(p.onTick(tickEvent))
        
        self.assertEqual(len(p.tops), 3)
        self.assertEqual(len(p.bottoms), 4)
        self.assertEqual(len(p.top_trendlines), 2)
        self.assertEqual(len(p.bottom_trendlines), 2)
        
        
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()