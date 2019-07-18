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
        if len(epochs) < 2:
            return
        expandrate = self.unitsecs*1.0/(epochs[1]-epochs[0])
        
        st = epochs[0]
        ed = epochs[-1]
        if st == ed:
            return
        if ed < self.epochs[0] or st > self.epochs[-1]:
            return
        sti = -1
        edi = -1
        for i in range(len(self.epochs)):
            if sti == -1 and st <= self.epochs[i]:
                if i == 0:
                    sti = 0
                else:
                    sti = i-1
            if edi == -1 and ed <= self.epochs[i]:
                edi = i-1
        
        shiftidx = 0
        for i in range(len(epochs)):
            if epochs[i] >= self.epochs[sti]:
                shiftidx = i
                break
        
        if sti == -1:
            sti = 0
        if edi == -1:
            idxs = range(shiftidx, len(self.epochs))
            ax.plot(idxs, self.vals[sti:], 
                    color=self.color, linewidth=self.linewidth)
        
        else:
            idxs = range(shiftidx, edi+1+shiftidx-sti)
            ax.plot(idxs, self.vals[sti:edi+1],
                    color=self.color, linewidth=self.linewidth)
        
                 
        