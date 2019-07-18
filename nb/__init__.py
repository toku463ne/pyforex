'''
Created on 2019/04/13

@author: kot
'''
import plotly.offline
import lib
import env
plotly.offline.init_notebook_mode()

import charts.matohlcv as m

def plotOhlcv(instrument, granularity,
                 startstr, endstr, plotElemnts=[]):
    startep = lib.str2epoch(startstr, env.DATE_FORMAT_NORMAL)
    endep = lib.str2epoch(endstr, env.DATE_FORMAT_NORMAL)
    m.plot(instrument, granularity, startep, endep, plotElemnts)
