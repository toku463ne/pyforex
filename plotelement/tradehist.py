'''
Created on 2019/04/28

@author: kot
'''
from plotelement import PlotElement
import lib

import env

class PlotEleTradeHist(PlotElement):
    

    def __init__(self, eventqueue, sellcolor="r", buycolor="b",  
                 markersize=600, linewidth=1.5):
        self.eventqueue = eventqueue
        self.sellcolor = sellcolor
        self.buycolor = buycolor
        self.markersize = markersize
        self.linewidth = linewidth
        
    
    
    def plot(self, ax, epochs):
        qued = self.eventqueue.dict
        for k in qued:
            ev = qued[k]
            st = ev.start_time
            ed = ev.end_time
            if st == ed:
                continue
            if ed < epochs[0] or st > epochs[-1]:
                continue
            sti = -1
            edi = -1
            if ev.side == env.SIDE_BUY:
                color = self.buycolor
            else:
                color = self.sellcolor
            
            for i in range(len(epochs)):
                if sti == -1 and st <= epochs[i]:
                    sti = i
                if edi == -1 and ed < epochs[i]:
                    edi = i-1
            if sti != -1:
                ax.scatter(sti, ev.start_price, c=color, marker=">", 
                            s=600, 
                            alpha=0.7)
                ax.annotate("  %d\n  %.3f\n  %s\n%s" % (ev.id, ev.start_price, 
                                          lib.epoch2str(epochs[sti], "%m-%d\n%H:%M"),
                                          ev.desc), 
                            (sti, ev.start_price), size=30, color=color,
                            horizontalalignment="left",verticalalignment="top")
            if edi != -1:
                if ev.profit > 0:
                    marker = "o"
                else:
                    marker = "x"
                ax.scatter(edi, ev.end_price, c=color, marker=marker, 
                            s=600, 
                            alpha=0.7)
                ax.annotate("  %d\n  %.3f\n  %s" % (ev.id, ev.end_price, 
                                          lib.epoch2str(epochs[edi], "%m-%d\n%H:%M")), 
                            (edi, ev.end_price), size=30, color=color,
                            horizontalalignment="right",verticalalignment="bottom")
            '''
            start_price = 0
            end_price = 0
            start_time = 0
            end_time = 0
            if sti > 0:
                start_price = ev.start_price
                start_time = ev.start_time
                ax.scatter(sti, start_price, c=color, marker="o", 
                            s=300, 
                            alpha=0.7)
            if edi > 0:
                end_price = ev.end_price
                end_time = ev.end_time
                if ev.profit > 0:
                    marker = "o"
                else:
                    marker = "x"
                ax.scatter(edi, end_price, c=color, marker=marker, 
                            s=600, 
                            alpha=0.7)
                
            if st < epochs[-1] and ed > epochs[-1]:
                end_time = epochs[-1]
                edi = len(epochs)-1
            if ed > epochs[0] and st < epochs[0]:
                start_time = epochs[0]
                sti = 0
            if ed < epochs[0] or st > epochs[-1]:
                continue
            
            slope = (end_price-start_price)/(end_time-start_time)
            end_price = start_price + slope*(end_time - start_time)
            ax.plot([sti, edi], [start_price, end_price], 
                            color=color, linewidth=self.linewidth)
            '''
            
            
                