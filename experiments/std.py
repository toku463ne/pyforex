'''
Created on 2019/05/18

@author: kot
'''
import lib
import lib.getter as getterlib
import env
import numpy as np
import pandas as pd

startstr = "2019-04-02T00:00:00"
endstr = "2019-04-02T18:00:00"
instrument = "USD_JPY"
granularity = "M5"
ANAL_LEN = 12 * 6 #6hours
PRED_LEN = 12 #1hour

startep = lib.str2epoch(startstr, env.DATE_FORMAT_NORMAL)
endep = lib.str2epoch(endstr, env.DATE_FORMAT_NORMAL)

(tl,ol,hl,ll,cl,vl) = getterlib.getPrices(instrument, granularity, startep, endep)
df = pd.DataFrame(columns=["time", 
                           "price", 
                           "hl",
                           "u-hige",
                           "d-hige",
                           "oc",
                           "c",
                           "v",
                           "fc_max",
                           "fc_min"],
                  index=range(ANAL_LEN,len(tl)))

for i in range(ANAL_LEN,len(tl)-PRED_LEN):
    t = tl[i]
    o = ol[i]
    h = hl[i]
    l = ll[i]
    c = cl[i]
    v = vl[i]
    df.loc[i]["time"] = lib.epoch2str(t, "%H:%M")
    df.loc[i]["price"] = c
    
    
    on = np.array(ol[i-ANAL_LEN:i+1])
    hn = np.array(hl[i-ANAL_LEN:i+1])
    ln = np.array(ll[i-ANAL_LEN:i+1])
    cn = np.array(cl[i-ANAL_LEN:i+1])
    vn = np.array(vl[i-ANAL_LEN:i+1])

    fcn = np.array(cl[i:i+PRED_LEN])
    
    
    hln = (hn-ln)
    mhl = hln.mean()
    shl = hln.std()
    vhl = (h-l-mhl)/shl
    
    df.loc[i]["hl"] = vhl
    df.loc[i]["oc"] = (c-o)/(h-l)*vhl
    df.loc[i]["u-hige"] = (h-max(o,c))/(h-l)
    df.loc[i]["d-hige"] = (min(o,c)-l)/(h-l)
    df.loc[i]["c"] = (c-cn.mean())/cn.std()
    df.loc[i]["v"] = (v-vn.mean())/vn.std()
    fcv = (fcn-fcn.mean())/fcn.std()
    fcnow = fcv[0]
    df.loc[i]["fc_max"] = fcv.max() - fcnow
    df.loc[i]["fc_min"] = fcv.min() - fcnow
    
    
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)
    