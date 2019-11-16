'''
Created on 2019/03/27

@author: kot
'''
import unittest
import data_getter.mssql as msgetter
from data_getter.oanda import OandaGetter
import env
import lib
import lib.names as names

class Test(unittest.TestCase):
    
    
    
    def testGetH1MSSQLPrices(self):
        env.run_mode = env.MODE_UNITTEST
        from db.mssql import MSSQLDB
        msgetter.N_REQUEST_ROWS = 10
        d = MSSQLDB()
        
        instrument = "USD_JPY"
        granularity = "M5"
        pTable = names.getPriceTable(instrument, granularity)
        d.execute("drop table if exists %s;" % pTable)
        
        fmt = "%Y/%m/%d %H:%M"
        og = msgetter.MSSQLGetter(OandaGetter(instrument, granularity))
        
        def _verify(ststr, edstr, tcnt, rcnt, openp, vol):
            st = lib.str2epoch(ststr, fmt)
            ed = lib.str2epoch(edstr, fmt)
            t, o, h, l, c, v = og.getPrice(st, ed)
            self.assertEqual(d.countTable(pTable),tcnt)
            self.assertEqual(t[0], st)
            self.assertEqual(t[-1], ed)
            self.assertEqual(len(t), rcnt)
            self.assertEqual(v[0], vol)
            self.assertEqual(o[0], openp)
        
        # 11:00 - 11:20    
        _verify("2019/11/13 11:00", "2019/11/13 11:20", 5,5, 108.94, 39)
        
        # 11:00 - 11:40
        _verify("2019/11/13 11:30", "2019/11/13 11:40", 9,3, 108.963, 21)
        
        # 10:40 - 11:40
        _verify("2019/11/13 10:40", "2019/11/13 10:50", 13,3, 108.906, 32)
        
        # 10:35 - 11:40
        _verify("2019/11/13 10:35", "2019/11/13 10:55", 14,5, 108.916, 39)
        
        # 10:35 - 11:50
        _verify("2019/11/13 11:30", "2019/11/13 11:50", 16,5, 108.963, 21)
        
        # 10:35 - 12:50
        _verify("2019/11/13 11:30", "2019/11/13 12:50", 28,17, 108.963, 21)
        
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetOandaPrice']
    unittest.main()