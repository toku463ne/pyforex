'''
Created on 2019/05/18

@author: kot
'''
import lib
import lib.getter as getterlib
import env
from lib import tradelib
from event.info import InfoEvent
import numpy as np

ANAL_LEN = 5



def run(instrument, granularity, startep, endep):
    infoevents = []
    densl = []
    (tl,ol,hl,ll,cl,vl) = getterlib.getPrices(instrument, granularity, startep, endep)
    for i in range(ANAL_LEN,len(tl)):
        t = tl[i]
        o = ol[i]
        h = hl[i]
        l = ll[i]
        c = cl[i]
        v = vl[i]
        
            
        dens,m = tradelib.getDensity(hl[i-ANAL_LEN:i], 
                                             ll[i-ANAL_LEN:i], 
                                             cl[i-ANAL_LEN:i])
        if dens >= 0.8:
            infoevents.append(InfoEvent(t,m,
                                "density:\n %.3f" % dens,
                                color="k"))
        if dens > 0:
            densl.append(dens)
        print("%s | %.3f density=%.3f" % (lib.epoch2str(t),m,dens))
    dn = np.array(densl)
    print("density mean=%.3f std=%.3f" % (dn.mean(),dn.std()))
    return infoevents

if __name__ == "__main__":
    startstr = "2018-10-01T00:00:00"
    endstr = "2018-11-01T00:00:00"
    instrument = "USD_JPY"
    granularity = "M5"

    startep = lib.str2epoch(startstr, env.DATE_FORMAT_NORMAL)
    endep = lib.str2epoch(endstr, env.DATE_FORMAT_NORMAL)
    run(instrument, granularity, startep, endep)
    
print("finished")
