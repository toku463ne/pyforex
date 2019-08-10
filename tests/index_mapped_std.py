'''
Created on 2019/03/27

@author: kot
'''
import lib

import unittest
from index.mapped.std import STDMappedIndex
import env
import math

class STDMappedIndexTest(unittest.TestCase):


    def testNormal(self):
        map_cache_len=10
        def checkPriceList(stdmap, stopep):
            _, stopep = stdmap.subc.getTime(stopep)
            pi_mi = -1
            pi_ma = -1
            for pi in stdmap.latestPriceList.priceInfo.keys():
                if pi_mi == -1 or pi < pi_mi:
                    pi_mi = pi
                if pi_ma == -1 or pi > pi_ma:
                    pi_ma = pi
            
            data_mi = -1
            data_ma = -1
            
            u = stdmap.unitsecs
            cache_start_epoch = stopep - map_cache_len*u
            
            for t in stdmap.data.keys():
                if t < cache_start_epoch:
                    continue
                
                if t > stopep:
                    break
                (k, _) = stdmap.data[t]
                if data_mi == -1 or k < data_mi:
                    data_mi = k
                if data_ma == -1 or k > data_ma:
                    data_ma = k
            
            self.assertEqual(pi_mi, data_mi)
            self.assertEqual(pi_ma, data_ma)
            
        
        env.run_mode = env.MODE_SIMULATE
        st = lib.str2epoch("2019/04/01 00:00", "%Y/%m/%d %H:%M")
        ed = lib.str2epoch("2019/04/02 00:00", "%Y/%m/%d %H:%M")
        d = STDMappedIndex("USD_JPY", "H1", st, ed, 
                           anal_span=5, 
                           maxsize=20, 
                           map_cache_len=map_cache_len)
        u = d.unitsecs
        
        self.assertEqual(len(d.data), 24)
        self.assertTrue(st in d.data.keys())
        self.assertTrue(ed-u in d.data.keys())
        
        # first value
        self.assertEqual(d.data[st][0],110.94)
        self.assertEqual(math.floor(d.data[st][1]*1000),84)
        
        # last value
        self.assertEqual(d.data[ed-u][0],111.38)
        self.assertEqual(math.floor(d.data[ed-u][1]*1000),41)
        
        from event.tick import TickEvent
        ep = lib.str2epoch("2019/04/01 15:00", "%Y/%m/%d %H:%M")
        tickEvent = TickEvent(ep, 1, 1)
        d.onTick(tickEvent)
        checkPriceList(d, ep)
        
        self.assertEqual(len(d.data), 24)
        self.assertTrue(st in d.data.keys())
        self.assertTrue(ed-u in d.data.keys())
        
        (cnt, min_edge, max_edge) = d.sumNearest(111.02, 2)
        self.assertEqual(cnt, 7)
        self.assertEqual(math.floor(min_edge*100), 11086)
        self.assertEqual(math.floor(max_edge*100), 11117)
        
        
        
        tickEvent = TickEvent(ed-1, 1, 1)
        d.onTick(tickEvent)
        self.assertEqual(len(d.data), 24)
        self.assertTrue(st in d.data.keys())
        self.assertTrue(ed-u in d.data.keys())
        
        checkPriceList(d, ed-1)
        
        tickEvent = TickEvent(ed, 1, 1)
        d.onTick(tickEvent)
        self.assertEqual(len(d.data), 25)
        self.assertTrue(st in d.data.keys())
        self.assertTrue(ed-u in d.data.keys())
        
        checkPriceList(d, ed)
        
        ep = lib.str2epoch("2019/04/02 10:00", "%Y/%m/%d %H:%M")
        tickEvent = TickEvent(ep, 1, 1)
        d.onTick(tickEvent)
        self.assertEqual(len(d.data), 20)
        self.assertFalse(st in d.data.keys())
        self.assertTrue(ed in d.data.keys())
        self.assertTrue(ep - u in d.data.keys())
        checkPriceList(d, ep)
        
        
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetOandaPrice']
    unittest.main()