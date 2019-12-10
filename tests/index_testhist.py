'''
Created on 2019/12/09

@author: kot
'''
import unittest
import lib
from index.testhistindex import TestHistIndex
import const_candles

class TestTestHistIndex(unittest.TestCase):
    def testCase1(self):
        t = TestHistIndex()
        print(t)
        hist = t.hist
        
        epoch = lib.str2epoch("2019-11-27T18:10:00")
        self.assertEqual(hist[epoch][0].pos, const_candles.LINEDIST_ABOVE_NEAR)
        
        epoch = lib.str2epoch("2019-11-27T18:15:00")
        self.assertEqual(hist[epoch], None)
        
        epoch = lib.str2epoch("2019-11-27T18:40:00")
        self.assertEqual(hist[epoch][0].pos, const_candles.LINEDIST_CROSSED)
        
        epoch = lib.str2epoch("2019-11-27T19:20:00")
        self.assertEqual(hist[epoch], None)
        
        epoch = lib.str2epoch("2019-11-27T19:30:00")
        self.assertEqual(hist[epoch][0].pos, const_candles.LINEDIST_CROSSED)
        
        epoch = lib.str2epoch("2019-11-27T23:00:00")
        self.assertEqual(hist[epoch][0].pos, const_candles.LINEDIST_CROSSED)
        self.assertEqual(hist[epoch][1].pos, const_candles.LINEDIST_ABOVE_NEAR)
        
        