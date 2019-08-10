'''
Created on 2019/03/27

@author: kot
'''
import lib

import unittest
from index.checker import CheckIndex
import env
import numpy as np

class CheckerIndexTest(unittest.TestCase):


    def testDow(self):
        env.run_mode = env.MODE_SIMULATE
        st = lib.str2epoch("2019/04/24 00:00", "%Y/%m/%d %H:%M")
        ed = lib.str2epoch("2019/04/25 00:00", "%Y/%m/%d %H:%M")
        d = CheckIndex("USD_JPY", "H1", st, ed)
        u = d.unitsecs
        
        from event.tick import TickEvent
        ep = lib.str2epoch("2019/04/24 01:00", "%Y/%m/%d %H:%M")
        
        udow_res = []
        ldow_res = []
        winl = []
        hours = []
        dts = []
        for _ in range(0, 24):
            tickEvent = TickEvent(ep, 1, 1)
            d.onTick(tickEvent)
            udow_res.append(d.isDowCandle(1))
            ldow_res.append(d.isDowCandle(-1))
            winl.append(d.isWindowOpen(0.01))
            hours.append(d.isHourRange(14, 17))
            dts.append(lib.epoch2dt(ep).hour)
            self.assertEqual(d.nowidx, d.subc.nowidx)
            self.assertEqual(d.now, d.subc.now)
            
            ep += u
            
        
        hl = np.array(d.subc.prices[2])
        ll = np.array(d.subc.prices[3])
        
        u1 = [((hl[i] > hl[i-1]) and (ll[i] > ll[i-1])) for i in range(1,len(hl))]
        l1 = [((hl[i] < hl[i-1]) and (ll[i] < ll[i-1])) for i in range(1,len(hl))]
        w = [False]*len(winl)
        w[20] = True
        hr = [False]*len(winl)
        hr[13] = True
        hr[14] = True
        hr[15] = True
        hr[16] = True
        
        self.assertListEqual(udow_res, u1, "upper dow")
        self.assertListEqual(ldow_res, l1, "down dow")
        self.assertListEqual(winl, w, "window open")
        self.assertListEqual(hours, hr, "hour range")
        
        
        
    def testWeekends(self):
        st = lib.str2epoch("2019/04/19 15:00", "%Y/%m/%d %H:%M")
        ed = lib.str2epoch("2019/04/22 03:00", "%Y/%m/%d %H:%M")
        d = CheckIndex("USD_JPY", "H1", st, ed)
        u = d.unitsecs
        
        from event.tick import TickEvent
        t = d.subc.prices[0]
        ep = st
        eps = []
        befwd = []
        aftwd1 = []
        aftwd2 = []
        aftwd3 = []
        for i in range(0, len(t)):
            ep = t[i]
            tickEvent = TickEvent(ep, 1, 1)
            d.onTick(tickEvent)
            dt = lib.epoch2dt(ep)
            eps.append("%d %d" % (dt.day, dt.hour))
            befwd.append(d.isNHoursBeforeWeekend(2))
            aftwd1.append(d.isNHoursAfterWeekend(1))
            aftwd2.append(d.isNHoursAfterWeekend(2))
            aftwd3.append(d.isNHoursAfterWeekend(3))
            
        
        befwd_a = [True, True, True, False, False, 
                   False, False, False, True, True, 
                   True, True, True]
        self.assertListEqual(befwd, befwd_a, "beyond 2h before weekend")
            
        aftwd1_a = [True, True, True, True, True, 
                  False, False, False, False, True, 
                  True, True, True]
        self.assertListEqual(aftwd1, aftwd1_a, "over 1h after weekend")
        '''
        eps = 
        ['19 15', '19 16', '19 17', '19 18', '19 19', 
         '19 20', '21 21', '21 22', '21 23', '22 0', 
         '22 1',  '22 2',  '22 3']
        '''
 
        aftwd2_a = [True, True, True, True, True, 
                  False, False, False, False, False, 
                  True, True, True]
        self.assertListEqual(aftwd2, aftwd2_a, "over 2h after weekend")
        
    
        aftwd3_a = [True, True, True, True, True, 
                  False, False, False, False, False, 
                  False, True, True]
        self.assertListEqual(aftwd3, aftwd3_a, "over 3h after weekend")
        
    
    def testResume(self):
        env.run_mode = env.MODE_SIMULATE
        st = lib.str2epoch("2019/04/24 00:00", "%Y/%m/%d %H:%M")
        ed = lib.str2epoch("2019/04/25 00:00", "%Y/%m/%d %H:%M")
        d = CheckIndex("USD_JPY", "H1", st, ed)
        u = d.unitsecs
        
        from event.tick import TickEvent
        ep = lib.str2epoch("2019/04/24 01:00", "%Y/%m/%d %H:%M")
        
        tickEvent = TickEvent(ep, 1, 1)
        d.onTick(tickEvent)
        self.assertTrue(d.isNextOK())    
        
        d.addForNext(5)
        
        ep += 4 * u
        tickEvent = TickEvent(ep, 1, 1)
        d.onTick(tickEvent)
        self.assertFalse(d.isNextOK())    
        
        ep += 1 * u
        tickEvent = TickEvent(ep, 1, 1)
        d.onTick(tickEvent)
        self.assertTrue(d.isNextOK())    
        
        d.addForNext(5)
        ep += 1 * u
        tickEvent = TickEvent(ep, 1, 1)
        d.addForNext(3)
        ep += 4 * u
        tickEvent = TickEvent(ep, 1, 1)
        d.onTick(tickEvent)
        self.assertFalse(d.isNextOK())    
        ep += 2 * u
        tickEvent = TickEvent(ep, 1, 1)
        d.onTick(tickEvent)
        self.assertFalse(d.isNextOK())    
        ep += 1 * u
        tickEvent = TickEvent(ep, 1, 1)
        d.onTick(tickEvent)
        self.assertTrue(d.isNextOK())    
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetOandaPrice']
    unittest.main()