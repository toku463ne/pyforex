'''
Created on 2019/05/01

@author: kot
'''
import unittest
from index.std import StdIndex
from event.tick import TickEvent
import lib
import env

class TestIndexStd(unittest.TestCase):


    def testIndexStd(self):
        instrument = "USD_JPY"
        granularity = "M5"
        std_span = 5
        startstr = "2019-04-02T09:00:00"
        endstr = "2019-04-02T11:30:00"
        startep = lib.str2epoch(startstr, env.DATE_FORMAT_NORMAL)
        endep = lib.str2epoch(endstr, env.DATE_FORMAT_NORMAL)
        
        s = StdIndex(instrument, granularity, startep, endep, std_span)
        
        epochstr = "2019-04-02T10:00:00"
        epoch = lib.str2epoch(epochstr, env.DATE_FORMAT_NORMAL)
        event = TickEvent(epoch,0,0)
        s.onTick(event)
        self.assertEqual(0.014709936173286954, s.get(), "std at %s" % epochstr)
    
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()