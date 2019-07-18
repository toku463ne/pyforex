'''
Created on 2019/04/13

@author: kot
'''

from data_getter import DataGetter
import env
import lib

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mpl_finance


class PandasGetter(DataGetter):
    def getPrice(self, startep, endep):
        (ep, o, h, l, c, v) = super(PandasGetter, self).getPrice(startep, endep)
        na = np.array([o, h, l, c, v])
        d = []
        for t in ep:
            d.append(lib.epoch2dt(t))
        
        df = pd.DataFrame(na.T, index=d, columns=["o", "h", "l", "c", "v"])
        return df
    

if __name__ == "__main__":
    from data_getter.mssql import MSSQLGetter
    from data_getter.oanda import OandaGetter
    
    env.run_mode = env.MODE_UNITTEST
    
    og = PandasGetter(MSSQLGetter(OandaGetter("USD_JPY", "H1")))
    
    st = lib.str2epoch("2019/04/02 07:00", "%Y/%m/%d %H:%M")
    ed = lib.str2epoch("2019/04/02 12:00", "%Y/%m/%d %H:%M")
    og.retrievePrice(st, ed)
    df = og.getPrice(st, ed)
    
    print(df)
    
    print("finished")
        