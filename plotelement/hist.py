'''
Created on 2019/04/28

@author: kot
'''
from plotelement import PlotElement
import lib
from tools.multiobjhistory import MultiObjHistory

class PlotEleHist(PlotElement):
    
    def __init__(self, multiObjHistory,   
                 markersize=600, linewidth=1.5):
        self.hist = multiObjHistory
        self.markersize = markersize
        self.linewidth = linewidth
    
    
    def plot(self, ax, epochs):      
        i = 0
        for (epoch, hes) in self.hist:
            while i < len(epochs) and epochs[i] < epoch:
                i += 1
                if i >= len(epochs):
                    break
                if epochs[i] >= epoch:
                    for he in hes:
                        price = he.price
                        if he.desc == "":
                            ax.scatter(i, price, c=he.color, marker=he.marker, 
                                        s=600)
                        else:
                            ax.annotate(he.desc, 
                                    (i, price), size=30, color=he.color,
                                    horizontalalignment="center")
                
        