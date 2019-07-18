'''
Created on 2019/05/18

@author: kot
'''
import lib
import lib.getter as getterlib
from tools.candleshape import CandleShape
import env
import numpy as np
from event.info import InfoEvent

ANAL_LEN = 12 #12hours


def run(instrument, granularity, startep, endep):
    cs = CandleShape()
    (tl,ol,hl,ll,cl,vl) = getterlib.getPrices(instrument, granularity, startep, endep)
    lenx = len(tl)-ANAL_LEN

    infoevents = []
    for i in range(ANAL_LEN,len(tl)-1):
        t1 = tl[i-1]
        o1 = ol[i-1]
        h1 = hl[i-1]
        l1 = ll[i-1]
        c1 = cl[i-1]
        v1 = vl[i-1]
        t2 = tl[i]
        o2 = ol[i]
        h2 = hl[i]
        l2 = ll[i]
        c2 = cl[i]
        v2 = vl[i]
        t3 = tl[i+1]
        o3 = ol[i+1]
        h3 = hl[i+1]
        l3 = ll[i+1]
        c3 = cl[i+1]
        v3 = vl[i+1]
        
        if (c2<o2) != (c1<o1):
            continue
        if c2 == o1:
            continue
        
        (size1, n1) = cs.classify(o1, h1, l1, c1)
        (size2, n2) = cs.classify(o2, h2, l2, c2)
        (dr1,_,_,_) = size1
        (dr2,_,_,_) = size1
        
        dr = dr2
        
        # daw
        if h1*dr1 > h2*dr:
            continue
        if l1*dr1 > l2*dr:
            continue
        
        
        on = np.array(ol[i-ANAL_LEN:i+1])
        hn = np.array(hl[i-ANAL_LEN:i+1])
        ln = np.array(ll[i-ANAL_LEN:i+1])
        cn = np.array(cl[i-ANAL_LEN:i+1])
        vn = np.array(vl[i-ANAL_LEN:i+1])
            
        hln = (hn-ln)
        me_hl = hln.mean()
        st_hl = hln.std()
        me_c = cn.mean()
        st_c = cn.std()
        
        hl1 = (h1-l1-me_hl)/st_hl
        hl2 = (h2-l2-me_hl)/st_hl
        
        #if h2-l2 < h1-l1:
        #    continue
        
        ocn = np.abs(cn-on)
        me_oc = ocn.mean()
        st_oc = ocn.std()
        oc1 = (abs(c1-o1)-me_oc)/st_oc
        oc2 = (abs(c2-o2)-me_oc)/st_oc
        if oc2 < oc1:
            continue
        if oc2 < 0:
            continue
        
        vc1 = (c1-me_c)/st_c
        vc2 = (c2-me_c)/st_c
        
        if vc1*dr < 0 or vc2*dr < 0:
            continue
        
        profit = (c3-c2)*dr/st_c
        
        color = "k"
        if dr == 1:
            color = "blue"
        if dr == -1:
            color = "red"
        infoevents.append(InfoEvent(t2,c2,
                        "shape:\n %s\n %s" % (str(size1),str(size2)),
                        color=color))
        print("%s | %.3f : dr=%d c1=%.3f c2=%.3f hl1=%.3f hl2=%.3f 1=%s 2=%s" % \
              (lib.epoch2str(t2), profit, dr,
              vc1,vc2,hl1,hl2,str(size1),str(size2)))
    return infoevents
        
if __name__ == "__main__":
    startstr = "2018-10-01T00:00:00"
    endstr = "2019-01-01T00:00:00"
    instrument = "USD_JPY"
    granularity = "H1"
    startep = lib.str2epoch(startstr, env.DATE_FORMAT_NORMAL)
    endep = lib.str2epoch(endstr, env.DATE_FORMAT_NORMAL)
    run(instrument, granularity, startep, endep)
    print("finished")