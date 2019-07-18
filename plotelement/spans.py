'''
Created on 2019/04/28

@author: kot
'''
from plotelement import PlotElement
import lib


class PlotEleSpans(PlotElement):
    

    def __init__(self, span="d", color="silver"):
        self.span = span
        self.color = color
    
    def plot(self, ax, epochs):
        for i in range(len(epochs)):
            ep = epochs[i]
            d = lib.epoch2dt(ep)
            if self.span == "d":
                if d.hour == 0 and d.minute == 0:
                    ax.axvline(i, label="%d-%d" % (d.month,d.day),c=self.color)
        
            
                