'''
Created on 2019/03/27

@author: kot
'''
import lib

import unittest
from tools.subchart import SubChart
import env

class SubChartTest(unittest.TestCase):


    def testNormal(self):
        env.run_mode = env.MODE_SIMULATE
        st = lib.str2epoch("2019/04/02 09:00", "%Y/%m/%d %H:%M")
        ed = lib.str2epoch("2019/04/02 12:00", "%Y/%m/%d %H:%M")
        s = SubChart("testNormal", "USD_JPY", "M5", st, ed, 5, 48)
        u = s.unitsecs
        
        (t,_,_,_,_,_) = s.getPrices()
        self.assertEqual(len(t), len(s.prices[0]))
        
        # 1
        i, now = s.getTime(st + 100)
        self.assertEqual(i,5)
        self.assertEqual(now,1554195600)
        
        # 2
        i, now = s.getTime(st + 400)
        self.assertEqual(i,6)
        self.assertEqual(now,1554195900)
        
        # 3
        i, now = s.getTime(ed + 400)
        self.assertEqual(i,42)
        self.assertEqual(now,1554206700)
        
        # 4
        i, now = s.getTime(ed - 500)
        self.assertEqual(i,39)
        self.assertEqual(now,1554205800)
        
        
        from event.tick import TickEvent
        tickEvent = TickEvent(1554196200+100, 1, 1)
        s.onTick(tickEvent)
        (t,o,h,l,c,v) = s.getPrices()
        self.assertEqual(t[-1], 1554196200)
        self.assertEqual(o[-1], 111.372)
        self.assertEqual(v[-1], 22)
        
        (t,o,h,l,c,v) = s.getPrices(5)
        self.assertEqual(t[0], 1554195600)
        self.assertEqual(t[-1], 1554196200)
        
        (t,o,h,l,c,v) = s.getPrices(5,6)
        self.assertEqual(t[-1], 1554195900)
        
        ep = ed + u*(48-len(s.prices[0])+48*0.5+1)
        tickEvent = TickEvent(ep, 1, 1)
        s.onTick(tickEvent)
        self.assertEqual(len(s.prices[0]), 48+48*0.5)
        (t,_,_,_,_,_) = s.getPrices()
        self.assertEqual(t[-1],ep)
        
        ep = t[-1] + u
        tickEvent = TickEvent(ep+100, 1, 1)
        s.onTick(tickEvent)
        self.assertEqual(len(s.prices[0]), 48)
        (t,_,_,_,_,_) = s.getPrices()
        self.assertEqual(t[-1],ep)
        
        
    def testWeekends(self):
        st = lib.str2epoch("2019/04/05 20:00", "%Y/%m/%d %H:%M")
        ed = lib.str2epoch("2019/04/08 01:00", "%Y/%m/%d %H:%M")
        s = SubChart("testWeekends", "USD_JPY", "H1", st, ed, 5)
        u = s.unitsecs
        
        i, now = s.getTime(st + 100)
        self.assertEqual(i,5)
        self.assertEqual(now,1554494400)
        
        i, now = s.getTime(st + u + 100)
        self.assertEqual(i,-1)
        
        i, now = s.getTime(1554670800 -u + 100)
        self.assertEqual(i,-1)
        
        i, now = s.getTime(1554670800 + 100)
        self.assertEqual(i,6)
        self.assertEqual(now,1554670800)
        
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetOandaPrice']
    unittest.main()