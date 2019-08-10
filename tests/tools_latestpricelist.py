'''
Created on 2019/08/03

@author: kot
'''
import lib

import unittest
from tools.latestpricelist import LatestPriceList
import env

class LatestPriceListTest(unittest.TestCase):
    def test(self):
        l = LatestPriceList(300, "USD_JPY")
        l.upsert(1000, 100.011, "test01")
        
        (s1, c1) = l.searchObj(100.012)
        self.assertEqual(s1, "test01")
        self.assertEqual(c1, 1)
        
        l.upsert(1010, 100.021, "test02")
        (s2, c2) = l.searchObj(100.022)
        self.assertEqual(s2, "test02")
        self.assertEqual(c2, 1)
        
        l.upsert(1020, 100.012, "test03")
        (s3, c3) = l.searchObj(100.013)
        self.assertEqual(s3, "test03")
        self.assertEqual(c3, 2)
        
        (s2, c2) = l.searchObj(100.023)
        self.assertEqual(s2, "test02")
        self.assertEqual(c2, 1)
        
        l.upsert(1320, 100.032, "test04")
        
        (s3, c3) = l.searchObj(100.013)
        self.assertEqual(s3, "test03")
        self.assertEqual(c3, 2)
        
        l.upsert(1321, 100.102, "test05")
        
        (s3, c3) = l.searchObj(100.011)
        self.assertEqual(s3, None, "time expiration")
        self.assertEqual(c3, 0)
        
        (s4, c4) = l.searchObj(100.036)
        self.assertEqual(s4, "test04")
        self.assertEqual(c4, 1)
        
        (s5, c5) = l.searchObj(100.106)
        self.assertEqual(s5, "test05")
        self.assertEqual(c5, 1)
        
        l.upsert(1330, 100.022, "test06")
        l.upsert(1331, 100.122, "test07")
        
        (lv, uv) = l.searchNearest(100.056)
        self.assertEqual(lv, 100.03)
        self.assertEqual(uv, 100.10)
        
        (lv, uv) = l.searchNearest(99.006)
        self.assertEqual(lv, -1)
        self.assertEqual(uv, 100.02)
        
        (lv, uv) = l.searchNearest(100.146)
        self.assertEqual(lv, 100.12)
        self.assertEqual(uv, -1)
        
        (lv, uv) = l.searchNearest(100.12)
        self.assertEqual(lv, 100.1)
        self.assertEqual(uv, 100.12)
        
        l.upsert(1322, 100.012, "test03")
        (s3, c3) = l.searchObj(100.013)
        self.assertEqual(s3, "test03")
        self.assertEqual(c3, 1)
        