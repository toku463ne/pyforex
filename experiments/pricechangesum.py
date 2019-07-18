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
        
map = peaks.maxpeaks
mip = peaks.minpeaks
(t,o,h,l,c,v) = peaks.getPrices()

mai = map.getKey(0)
mii = mip.getKey(0)
last_peaki = -1
next_peaki = -1
df = pd.DataFrame(columns=["time", "price", "sum", "peak_type", "lastt"],index=t)
last_peak_ep = 0
for ep in t:
    i,ep = peaks.subc.getTime(ep)
    val = 0
    dif = 0
    peak_type = 0
    if i == mai:
        peak_type = 1
    if i == mii:
        peak_type = -1
    if i == mai or i == mii:
        next_peaki = i
        
    if next_peaki > 0 and i-peak_span>next_peaki:
        last_peaki = next_peaki
    
    if last_peaki >= 0:
        for j in range(last_peaki,i+1):
            val += (c[j]-o[j])*v[j] 
        df.loc[ep]["time"] = lib.epoch2str(ep, "%H:%M")
        df.loc[ep]["price"] = c[i]
        df.loc[ep]["sum"] = val
        df.loc[ep]["peak_type"] = peak_type
        df.loc[ep]["lastt"] = lib.epoch2str(t[last_peaki], "%H:%M")

    
    if i == mai:
        idx = map.getIdx(mai)+1
        if idx < len(map):
            mai = map.getKey(idx)
    if i == mii:
        idx = mip.getIdx(mii)+1
        if idx < len(mip):
            mii = mip.getKey(idx)
    
    
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)
    