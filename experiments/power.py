'''
Created on 2019/11/09

@author: kot
'''

import env
import lib
from index.power import PowerIndex

startep = lib.str2epoch("2019-10-17T20:00:00", env.DATE_FORMAT_NORMAL)
endep = lib.str2epoch("2019-10-20T00:00:00", env.DATE_FORMAT_NORMAL)
    
p = PowerIndex("USD_JPY", "M5", startep, endep, 12)

(t,o,h,l,c,v) = p.subc.prices
for i in range(len(p.epochs)):
    bu = p.bull_totals[i]
    be = p.bear_totals[i]
    print("%s price=%.3f bull_rate=%.3f bull_change=%.3f bear_change=%.3f" % (
        lib.epoch2str(p.epochs[i], env.DATE_FORMAT_NORMAL),
        c[i+p.sumspan],
        bu/(bu+be),
        p.bull[i]/bu, p.bear[i]/be
        ))
    