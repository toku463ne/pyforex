'''
Created on 2019/04/28

@author: kot
'''
from plotelement import PlotElement
import lib

class PlotEleEvents(PlotElement):
    

    def __init__(self, infoevents,   
                 markersize=600, linewidth=1.5):
        self.infoevents = infoevents
        self.markersize = markersize
        self.linewidth = linewidth
    
    
    def plot(self, ax, epochs):
        prices = []
        for ie in self.infoevents:
            if ie.ep >= epochs[0] and ie.ep <= epochs[-1]:
                prices.append(ie.price)
        if len(prices) == 0:
            return
        max_p = max(prices)
        min_p = min(prices)
        mdp = (max_p + min_p)/2
        
        def plot(ie, i):
            if ie.price >= mdp:
                va = "bottom"
            else:
                va = "top"
             
            price = ie.price
            ax.scatter(i, price, c=ie.color, marker=ie.marker, 
                            s=600)
            ax.annotate("  %.3f\n  %s\n %s" % (price, 
                        lib.epoch2str(ie.ep, "%m-%d\n%H:%M"), ie.info), 
                        (i, price), size=30, color=ie.color,
                        horizontalalignment="center",
                        verticalalignment=va)
        
        
        
        i = 0
        for ie in self.infoevents:
            while i < len(epochs) and epochs[i] < ie.ep:
                i += 1
                if i >= len(epochs):
                    break
                if epochs[i] >= ie.ep:
                    plot(ie, i)
                
        