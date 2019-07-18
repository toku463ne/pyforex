'''
Created on 2019/03/27

@author: kot
'''
import lib

import unittest
from data_getter.oanda import OandaGetter


class Test(unittest.TestCase):


    def testGetOandaPrice(self):
        st = lib.str2epoch("2019/04/02 09:00", "%Y/%m/%d %H:%M")
        ed = lib.str2epoch("2019/04/02 12:00", "%Y/%m/%d %H:%M")
        o = OandaGetter("USD_JPY", "H1")
        
        t, o, h, l, c, v = o.getPrice(st, ed)
        self.assertEqual(t[0], 1554195600)
        self.assertEqual(t[-1], 1554206400)
        self.assertEqual(len(t), 4)
        self.assertEqual(v[0], 372)
        self.assertEqual(o[0], 111.394)
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetOandaPrice']
    unittest.main()