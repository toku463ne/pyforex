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

ANAL_LEN = 20
MIN_LEG_LEN = 10

def run(instrument, granularity, startep, endep):
    cs = CandleShape()
    (tl,ol,hl,ll,cl,vl) = getterlib.getPrices(instrument, granularity, startep, endep)
    lenx = len(tl)-ANAL_LEN

    infoevents = []
    for i in range(ANAL_LEN,len(tl)-1):
        t1 = tl[i-2]
        o1 = ol[i-2]
        h1 = hl[i-2]
        l1 = ll[i-2]
        c1 = cl[i-2]
        v1 = vl[i-2]
        t2 = tl[i-1]
        o2 = ol[i-1]
        h2 = hl[i-1]
        l2 = ll[i-1]
        c2 = cl[i-1]
        v2 = vl[i-1]
        t3 = tl[i]
        o3 = ol[i]
        h3 = hl[i]
        l3 = ll[i]
        c3 = cl[i]
        v3 = vl[i]
        
        
        (size1, n1) = cs.classify(o1, h1, l1, c1)
        
        
        on = np.array(ol[i-ANAL_LEN:i+1])
        hn = np.array(hl[i-ANAL_LEN:i+1])
        ln = np.array(ll[i-ANAL_LEN:i+1])
        cn = np.array(cl[i-ANAL_LEN:i+1])
        vn = np.array(vl[i-ANAL_LEN:i+1])
        
        is_max_peak = True
        if h2 == hn[-MIN_LEG_LEN:].max():
            is_max_peak = True
        elif l2 == ln[-MIN_LEG_LEN:].min():
            is_max_peak = False
        else:
            continue
        
        me_c = cn.mean()
        st_c = cn.std()
        vc2 = (c2-me_c)/st_c
        
        
        (dr, p1,p2,p3) = size1
        if is_max_peak:
            if p1 > p3:
                continue
            if p3 < 2:
                continue
            if o2 < c2:
                if o3 < c3:
                    continue
            if max(c3,o3) >= o2:
                continue
            if max(c1,o1) > o2:
                continue
            #if vc2 < 1:
            #    continue
        else:
            if p1 < p3:
                continue
            if p2 > 2:
                continue
            if o2 > c2:
                if o3 > c3:
                    continue
            if min(c1,o1) < o2:
                continue
            if min(c3,o3) < o2:
                continue
            #if vc2 > -1:
            #    continue
        color = "k"
        if is_max_peak:
            color = "blue"
        else:
            color = "red"
        
        infoevents.append(InfoEvent(t2,c2,
                        "shape:\n %s" % (str(size1)),
                        color=color))
        print("%s | %.3f " % \
              (lib.epoch2str(t2), c2))
    return infoevents
        
if __name__ == "__main__":
    startstr = "2018-10-01T00:00:00"
    endstr = "2019-01-01T00:00:00"
    instrument = "USD_JPY"
    granularity = "M5"
    startep = lib.str2epoch(startstr, env.DATE_FORMAT_NORMAL)
    endep = lib.str2epoch(endstr, env.DATE_FORMAT_NORMAL)
    infoevents = run(instrument, granularity, startep, endep)
    print("finished")

    import charts.matohlcv as m
    from plotelement.events import PlotEleEvents
    evpe = PlotEleEvents(infoevents)
    m.plot(instrument, granularity, startep, endep, [evpe])
    