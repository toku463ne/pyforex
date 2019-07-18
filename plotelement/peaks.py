'''
Created on 2019/04/28

@author: kot
'''
from plotelement import PlotElement
import lib

class PlotElePeaks(PlotElement):
    

    def __init__(self, epochs, peaks, is_maxpeak=True, color="k",  
                 markersize=600, linewidth=1.5):
        self.peaks = peaks
        self.epochs = epochs
        self.color = color
        self.markersize = markersize
        self.linewidth = linewidth
        self.is_maxpeak = is_maxpeak
    
    
    def plot(self, ax, epochs):
        sep = self.epochs
        if self.is_maxpeak:
            verticalalignment = "bottom"
        else:
            verticalalignment = "top"
        
        def plot(_id, i):        
            price = self.peaks.get(_id)
            ax.scatter(i, price, c=self.color, marker="_", 
                            s=600)
            ax.annotate("  %.3f\n  %s" % (price, 
                        lib.epoch2str(self.epochs[_id], "%m-%d\n%H:%M")), 
                        (i, price), size=30, color=self.color,
                        horizontalalignment="center",
                        verticalalignment=verticalalignment)
        
        i = 0
        for _id in self.peaks.keys():
            while i < len(epochs) and epochs[i] < sep[_id]:
                i += 1
                if i >= len(epochs):
                    break
                if epochs[i] >= sep[_id]:
                    plot(_id, i)
                
        '''
        iep = self.epochs
        startep = epochs[0]
        starti = -1
        for i in range(len(iep)):
            if iep[i] >= startep:
                starti = i
                break
        
        for _id in self.peaks.keys():
            if _id < starti:
                continue
            if _id - starti > len(epochs)/expandrate-1:
                return
            price = self.peaks.get(_id)
            if self.is_maxpeak:
                verticalalignment = "bottom"
            else:
                verticalalignment = "top"
            x = (_id - starti)*expandrate
            ax.scatter(x, price, c=self.color, marker="_", 
                            s=600)
            ax.annotate("  %.3f\n  %s" % (price, 
                                      lib.epoch2str(self.epochs[_id], "%m-%d\n%H:%M")), 
                        (x, price), size=30, color=self.color,
                        horizontalalignment="center",
                        verticalalignment=verticalalignment)
        '''
        