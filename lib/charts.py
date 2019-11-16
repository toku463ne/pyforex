'''
Created on 2019/04/13

@author: kot
'''
import lib.getter as getter
import lib
import matplotlib.pyplot as plt
 
import math
import mpl_finance
import env

def plot_ohlc(ax, ep, o, h, l, c, datetime_display_span="h"):
    max_price = max(h)
    min_price = min(l)
    old_val = -1
    datecolor = "dodgerblue"
    do_show = False
    for i in range(len(ep)):
        t = ep[i]
        d = lib.epoch2dt(t)
        if datetime_display_span == "d":
            if d.hour == 0 and d.day != old_val:
                do_show = True
                old_val = d.day
        if datetime_display_span == "h":
            if d.minute == 0 and d.hour != old_val:
                do_show = True
                old_val = d.hour
                
                
        if do_show:    
            if c[i] >= (max_price+min_price)/2:
                yval = min_price
            else:
                yval = max_price
            ax.axvline(i, c=datecolor)
            ax.annotate("%02d-%02d\n%02d:%02d" % (int(d.month), 
                                                  int(d.day), 
                                                  int(d.hour), 
                                                  int(d.minute)), 
                (i, yval), size=30, color=datecolor,
                horizontalalignment="left")
            do_show = False  
    
    mid_price = (max_price+min_price)/2
    ax.axhline(y=max_price, color=datecolor)
    ax.annotate(max_price, (0, max_price), size=30, color=datecolor, horizontalalignment="right")
    ax.axhline(y=mid_price, color=datecolor)
    ax.annotate(mid_price, (0, mid_price), size=30, color=datecolor, horizontalalignment="right")
    ax.axhline(y=min_price, color=datecolor)
    ax.annotate(min_price, (0, min_price), size=30, color=datecolor, horizontalalignment="right")
    mpl_finance.candlestick2_ohlc(ax, opens=o, closes=c,lows=l, highs=h,
                          width=0.8, colorup='lightgray', colordown='grey', alpha=1)
    

def plot(instrument, granularity,
                 startep, endep,
                 plotElements=[], datetime_display_span="d"):
        
    (ep, o, h, l, c, v) = getter.getPrices(instrument, granularity, startep, endep)
    
    nbars = len(ep)
    nbar = env.CHART_NBARS_PER_CHART
    nrows = math.ceil(nbars*1.0/env.CHART_NBARS_PER_CHART)
    #unitsecs = tradelib.getUnitSecs(granularity)
    
    fig = plt.figure(figsize=(50, 15*nrows))
    i = 0
    sti = 0
    for i in range(nrows):
        ax = fig.add_subplot(nrows, 1, i+1)
        eps = ep[sti:sti+nbar]
        if len(eps) == 0:
            break
        plot_ohlc(ax, eps, o[sti:sti+nbar], 
                   h[sti:sti+nbar], l[sti:sti+nbar], c[sti:sti+nbar], 
                   datetime_display_span=datetime_display_span)
        for pe in plotElements:
            if pe != None:
                pe.plot(ax, eps)
        sti += nbar
        
    fig.autofmt_xdate()
    fig.tight_layout()

def getDefaultPlotEleTradeHist(transaction_name,
                          startep=-1, endep=-1):
    from portfolio.mssql import MSSQLPortfolio
    from plotelement.tradehist import PlotEleTradeHist
    po = MSSQLPortfolio(transaction_name)
    eq = po.getTradeHistoryEventQueue(startep, endep)
    _, ev = eq.getFirst()
    startep = ev.startep
    _, ev = eq.getLast()
    endep = ev.endep
    tradehist = PlotEleTradeHist(eq)
    return tradehist, startep, endep

def str2epoch_sted(startstr="", endstr=""):
    if startstr == "":
        startep = -1
    else:
        startep = lib.str2epoch(startstr, env.DATE_FORMAT_NORMAL)
    if endstr == "":
        endep = -1
    else:
        endep = lib.str2epoch(endstr, env.DATE_FORMAT_NORMAL)
    return startep, endep


if __name__ == "__main__":
    #startep = lib.str2epoch("2019-04-02T09:00:00", env.DATE_FORMAT_NORMAL)
    #endep = lib.str2epoch("2019-04-02T14:10:00", env.DATE_FORMAT_NORMAL)
    #plot("USD_JPY", "M1", startep, endep)
    pass
