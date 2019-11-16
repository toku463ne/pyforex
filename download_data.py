'''
Created on 2019/04/13

@author: kot
'''

import lib
from data_getter.mssql import MSSQLGetter
from data_getter.oanda import OandaGetter
import datetime

if __name__ == "__main__":
    og = MSSQLGetter(OandaGetter("USD_JPY", "M1"))
    st = datetime.datetime(2019,1,1,0,0,0)
    ed = datetime.datetime(2019,11,13,0,0,0)
    og.getPrice(lib.dt2epoch(st), lib.dt2epoch(ed))
    
    print("finished")
    