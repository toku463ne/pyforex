'''
Created on 2019/05/06

@author: kot
'''

from index.peaks import PeaksIndex
import lib
import env
import pandas as pd

startstr = "2019-04-02T09:00:00"
endstr = "2019-04-02T18:00:00"
instrument = "USD_JPY"
granularity = "M5"
startep = lib.str2epoch(startstr, env.DATE_FORMAT_NORMAL)
endep = lib.str2epoch(endstr, env.DATE_FORMAT_NORMAL)

peak_span = 5
peaks = PeaksIndex(instrument, granularity, startep, endep, 10, 
                 peak_span, collect_last_changes=False)
sum_nbars = 25

(t,o,h,l,c,v) = peaks.getPrices()

df = pd.DataFrame(columns=["time", "price", "sum"],index=range(len(t)))
last_peak_ep = 0

for i in range(sum_nbars-1,len(t)):
    val = 0
    dif = 0
    
    for j in range(i-sum_nbars,i+1):
        val += (c[j]-o[j])*v[j] 
        df.loc[i]["time"] = lib.epoch2str(t[i], "%H:%M")
    df.loc[i]["price"] = c[i]
    df.loc[i]["sum"] = val

        
    
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)
    