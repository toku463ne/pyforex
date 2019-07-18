'''
Created on 2019/04/27

@author: kot
'''
import unittest
from backtests import runDollCost
import lib
import env


class ForexDollCost(unittest.TestCase):


    def testDollCost(self):
        startstr = "2019-04-01T00:00:00"
        endstr = "2019-05-01T00:00:00"
        instr = "USD_JPY"
        startep = lib.str2epoch(startstr, env.DATE_FORMAT_NORMAL)
        endep = lib.str2epoch(endstr, env.DATE_FORMAT_NORMAL)
        
        po, pe = runDollCost(instr, startstr, endstr)
        po.getSum("d")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    