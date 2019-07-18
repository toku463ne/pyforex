'''
Created on 2019/04/28

@author: kot
'''
from plotelement import PlotElement
import lib

import env

class PlotEleLineChart(PlotElement):
    

    def __init__(self, epochs, vals,  
                 color="green", linewidth=1.5):
        self.color = color
        self.epochs = epochs
        self.vals = vals
        self.linewidth = linewidth
    
    
    def plot(self, ax, epochs):
        sep = self.epochs
        i = 0
        idxs = []
        vals = []
        #if epochs[0] >= sep[0]:
        #    idxs.append(i)
        #    vals.append(self.vals[i])
        for j in range(len(sep)):
            while i < len(epochs) and epochs[i] < sep[j]:
                i += 1
                if i >= len(epochs):
                    break
                if epochs[i] >= sep[j]:
                    idxs.append(i)
                    vals.append(self.vals[j])
                
        
        ax.plot(idxs, vals,
                    color=self.color, linewidth=self.linewidth)
        
        
                 
        