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
    def testGetM5MSSQLPrices(self):
        env.run_mode = env.MODE_UNITTEST
        from db.mssql import MSSQLDB
        d = MSSQLDB()
        
        instrument = "USD_JPY"
        granularity = "M5"
        pTable = names.getPriceTable(instrument, granularity)
        mTable = names.getMetainfTable(instrument, granularity)
        d.execute("drop table if exists %s;" % pTable)
        d.execute("drop table if exists %s;" % mTable)
        
        msgetter.N_REQUEST_ROWS = 10
        og = msgetter.MSSQLGetter(OandaGetter(instrument, granularity))
        st = lib.str2epoch("2019/04/02 09:00", "%Y/%m/%d %H:%M")
        ed = lib.str2epoch("2019/04/02 12:00", "%Y/%m/%d %H:%M")
        _, _, _, _, _, _ = og.getPrice(st, ed)
        self.assertEqual(d.countTable(mTable),1)
        self.assertEqual(d.countTable(pTable),37)
        

    def testGetH1MSSQLPrices(self):
        env.run_mode = env.MODE_UNITTEST
        from db.mssql import MSSQLDB
        d = MSSQLDB()
        
        instrument = "USD_JPY"
        granularity = "H1"
        pTable = names.getPriceTable(instrument, granularity)
        mTable = names.getMetainfTable(instrument, granularity)
        d.execute("drop table if exists %s;" % pTable)
        d.execute("drop table if exists %s;" % mTable)
        
        og = msgetter.MSSQLGetter(OandaGetter(instrument, granularity))
        st = lib.str2epoch("2019/04/02 09:00", "%Y/%m/%d %H:%M")
        ed = lib.str2epoch("2019/04/02 12:00", "%Y/%m/%d %H:%M")
        t, o, h, l, c, v = og.getPrice(st, ed)
        self.assertEqual(d.countTable(mTable),1)
        self.assertEqual(d.countTable(pTable),4)
        self.assertEqual(t[0], 1554195600)
        self.assertEqual(t[-1], 1554206400)
        self.assertEqual(len(t), 4)
        self.assertEqual(v[0], 372)
        self.assertEqual(o[0], 111.394)
        
        
        st = lib.str2epoch("2019/04/02 15:00", "%Y/%m/%d %H:%M")
        ed = lib.str2epoch("2019/04/02 17:00", "%Y/%m/%d %H:%M")
        t, o, h, l, c, v = og.getPrice(st, ed)
        self.assertEqual(d.countTable(mTable),2)
        self.assertEqual(d.countTable(pTable),7)
        self.assertEqual(t[0], 1554217200)
        self.assertEqual(t[-1], 1554224400)
        self.assertEqual(len(t), 3)
        self.assertEqual(h[0], 111.342)
        self.assertEqual(l[0], 111.25)
        
        st = lib.str2epoch("2019/04/02 07:00", "%Y/%m/%d %H:%M")
        ed = lib.str2epoch("2019/04/02 10:00", "%Y/%m/%d %H:%M")
        t, o, h, l, c, v = og.getPrice(st, ed)
        self.assertEqual(d.countTable(mTable),2)
        self.assertEqual(d.countTable(pTable),9)
        self.assertEqual(t[0], 1554188400)
        self.assertEqual(t[-1], 1554199200)
        self.assertEqual(len(t), 4)
        self.assertEqual(v[1], 301)
        self.assertEqual(o[1], 111.372)
        
        st = lib.str2epoch("2019/04/02 14:00", "%Y/%m/%d %H:%M")
        ed = lib.str2epoch("2019/04/02 15:00", "%Y/%m/%d %H:%M")
        t, o, h, l, c, v = og.getPrice(st, ed)
        self.assertEqual(d.countTable(mTable),2)
        self.assertEqual(d.countTable(pTable),10)
        self.assertEqual(t[0], 1554213600)
        self.assertEqual(t[-1], 1554217200)
        self.assertEqual(len(t), 2)
        self.assertEqual(o[1], 111.302)
        self.assertEqual(c[1], 111.33)
        
        
        st = lib.str2epoch("2019/04/02 17:00", "%Y/%m/%d %H:%M")
        ed = lib.str2epoch("2019/04/02 19:00", "%Y/%m/%d %H:%M")
        t, o, h, l, c, v = og.getPrice(st, ed)
        self.assertEqual(d.countTable(mTable),2)
        self.assertEqual(d.countTable(pTable),12)
        self.assertEqual(t[0], 1554224400)
        self.assertEqual(t[-1], 1554231600)
        self.assertEqual(len(t), 3)
        self.assertEqual(v[2], 255)
        self.assertEqual(o[2], 111.386)
        
        
        st = lib.str2epoch("2019/04/02 10:00", "%Y/%m/%d %H:%M")
        ed = lib.str2epoch("2019/04/02 20:00", "%Y/%m/%d %H:%M")
        t, o, h, l, c, v = og.getPrice(st, ed)
        self.assertEqual(d.countTable(mTable),1)
        self.assertEqual(d.countTable(pTable),14)
        self.assertEqual(t[0], 1554199200)
        self.assertEqual(t[-1], 1554235200)
        self.assertEqual(len(t), 11)
        self.assertEqual(o[5], 111.302)
        self.assertEqual(c[5], 111.33)
        

        st = lib.str2epoch("2019/04/01 00:00", "%Y/%m/%d %H:%M")
        ed = lib.str2epoch("2019/04/01 03:00", "%Y/%m/%d %H:%M")
        t, o, h, l, c, v = og.getPrice(st, ed)
        self.assertEqual(d.countTable(mTable),2)
        self.assertEqual(d.countTable(pTable),18)
        self.assertEqual(len(t), 4)
        
        st = lib.str2epoch("2019/04/01 03:00", "%Y/%m/%d %H:%M")
        ed = lib.str2epoch("2019/04/01 06:00", "%Y/%m/%d %H:%M")
        t, o, h, l, c, v = og.getPrice(st, ed)
        self.assertEqual(d.countTable(mTable),2)
        self.assertEqual(d.countTable(pTable),21)
        self.assertEqual(len(t), 4)
        
        st = lib.str2epoch("2019/04/01 07:00", "%Y/%m/%d %H:%M")
        ed = lib.str2epoch("2019/04/02 09:00", "%Y/%m/%d %H:%M")
        t, o, h, l, c, v = og.getPrice(st, ed)
        self.assertEqual(d.countTable(mTable),1)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetOandaPrice']
    unittest.main()