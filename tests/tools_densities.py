'''
Created on 2019/03/27

@author: kot
'''
import lib

import unittest
from index.densities import DensityIndex
import env
import math

class DensitiesTest(unittest.TestCase):


    def testNormal(self):
        env.run_mode = env.MODE_SIMULATE
        st = lib.str2epoch("2019/04/03 00:00", "%Y/%m/%d %H:%M")
        ed = lib.str2epoch("2019/04/04 00:00", "%Y/%m/%d %H:%M")
        d = DensityIndex("USD_JPY", "H1", st, ed, 5)
        u = d.unitsecs
        d.printDens()
        
        self.assertEqual(len(d.densdata), 24)
        self.assertEqual(st, d.densdata[st].epoch)
        self.assertEqual(ed-u, d.densdata[ed-u].epoch)
        
        b = d.densdata[st]
        self.assertEqual(b.density, -1)
        self.assertEqual(b.mean, -1)
        self.assertEqual(b.std, -1)
        
        
        ep = lib.str2epoch("2019/04/03 11:00", "%Y/%m/%d %H:%M")
        b = d.densdata[ep]
        self.assertEqual(math.floor(b.density*100), 27)
        self.assertEqual(b.mean, 111.5)
        self.assertEqual(math.floor(b.std*10000), 99)
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetOandaPrice']
    unittest.main()