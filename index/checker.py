'''
Created on 2019/04/14

@author: kot
'''
from index import TechnicalIndex
from tools.subchart import SubChart
import math
import lib

class CheckIndex(TechnicalIndex):
    
    def __init__(self, instrument, granularity, startep=-1, endep=-1):
        super(CheckIndex, self).__init__(instrument, granularity)
        self.subc = SubChart(self.__class__.__name__, instrument, granularity, startep, 
                             endep)
        self.cntForNext = 0
        self.nowidx = -1
        self.now = -1
        
        
    def onTick(self, tickEvent):
        i, epoch = self.subc.onTick(tickEvent)
        if i == -1:
            return False
        if self.now == epoch:
            return
        if self.cntForNext > 0:
            self.cntForNext -= (epoch - self.now)/self.unitsecs
            if self.cntForNext < 0:
                self.cntForNext = 0
        self.nowidx = i
        self.now = epoch
        return True
        
    def isNextOK(self):
        if self.cntForNext == 0:
            return True
        else:
            return False
    
    def addForNext(self, cnt):
        self.cntForNext += cnt
        
    def getPriceAt(self, j=0):
        i = self.nowidx
        (t, ol, hl, ll, cl, vl) = self.subc.getPrices()
        k = i-j
        return (t[k], ol[k], hl[k], ll[k], cl[k], vl[k])
        
        
    #direction=1: up dow
    #direction=-1: down dow
    def isDowCandle(self, direction=1):
        try:
            i = self.nowidx
            (_, _, hl, ll, _, _) = self.subc.getPrices()
            if direction == 1:
                if hl[i]>hl[i-1] and ll[i]>ll[i-1]:
                    return True
                else:
                    return False
            elif direction == -1:
                if hl[i]<hl[i-1] and ll[i]<ll[i-1]:
                    return True
                else:
                    return False
            else:
                return False
        except IndexError:
            lib.printError(self.now, "index error: i=%d len(hl)=%d len(ll)=%d" % (
                i, len(hl), len(ll)))
            raise IndexError
            
        
    def isWindowOpen(self, wsize=0):
        i = self.nowidx
        (_, _, hl, ll, _, _) = self.subc.getPrices()
        if hl[i]+wsize < ll[i-1] or ll[i]-wsize > hl[i-1]:
            return True
        return False
            
            
    def isHourRange(self, startHour, endHour):
        eh = (self.now % (3600 * 24)) / 3600
        if eh >= startHour and eh <= endHour:
            return True
        return False
    
    def isNHoursBeforeWeekend(self, n):
        if self.isWeekend():
            return False
        if math.floor((self.now / (3600 * 24) + 4) % 7) == 5: #Friday
            if self.isHourRange(20-n, 21):
                return False
        return True
    
    def isNHoursAfterWeekend(self, n):
        if self.isWeekend():
            return False
        dn = math.floor((self.now / (3600 * 24) + 4) % 7)
        if dn == 0: #Sunday
            if self.isHourRange(22, 22+n):
                return False
        elif dn == 1 and n>=2: # Monday
            if self.isHourRange(22, 24) or self.isHourRange(0, n-2):
                return False
        return True
    
    
    # considering summer time, at this funtion 
    # weekend starts 1 hour earlier on winter
    # and ends 1 hour later on summer, to make always the same result
    # New York time 
    def isWeekend(self):
        dn = math.floor((self.now / (3600 * 24) + 4) % 7)
        if dn == 6: # Saturday
            return True
        elif dn == 0: # Sunday
            if self.isHourRange(0, 22):
                return True
        elif dn == 5: # Friday
            if self.isHourRange(20, 24):
                return True
        return False
    
        