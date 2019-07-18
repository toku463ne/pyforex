'''
Created on 2019/05/18

@author: kot
'''
import lib
import lib.getter as getterlib
import env
import numpy as np
import math
import pandas as pd

startstr = "2018-10-01T00:00:00"
endstr = "2018-11-01T00:00:00"
instrument = "USD_JPY"
granularity = "M5"
ANAL_LEN = 12 * 6 #6hours
PRED_LEN = 12 #1hour

startep = lib.str2epoch(startstr, env.DATE_FORMAT_NORMAL)
endep = lib.str2epoch(endstr, env.DATE_FORMAT_NORMAL)

(tl,ol,hl,ll,cl,vl) = getterlib.getPrices(instrument, granularity, startep, endep)
lenx = len(tl)-PRED_LEN-ANAL_LEN

a = np.zeros((lenx,6))
for i in range(ANAL_LEN,len(tl)-PRED_LEN):
    t = tl[i]
    o = ol[i]
    h = hl[i]
    l = ll[i]
    c = cl[i]
    v = vl[i]
    
    
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
    
    a[i-ANAL_LEN][0] = vhl #hl
    if vhl > 0:
        a[i-ANAL_LEN][1] = (c-o)/(h-l)*vhl #zittai
    if h-l > 0:
        a[i-ANAL_LEN][2] = (h-max(o,c))/(h-l) #u-hige
        a[i-ANAL_LEN][3] = (min(o,c)-l)/(h-l) #d-hige
    #a[i-ANAL_LEN][4] = (c-cn.mean())/cn.std() # close
    a[i-ANAL_LEN][4] = (v-vn.mean())/vn.std() # volume
    
b = []
for i in range(ANAL_LEN,len(tl)-PRED_LEN):
    for j in range(ANAL_LEN+i,len(tl)-PRED_LEN):
        if i != j:
            b.append(((a[i-ANAL_LEN]-a[j-ANAL_LEN])**2).sum())

bn = np.array(b)

print(bn.mean())
print(bn.std())
print(len(bn))
c = np.where(bn<0.5)[0]
print(len(c))
print(c)

print("finished")