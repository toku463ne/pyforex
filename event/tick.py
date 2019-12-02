'''
Created on 2019/04/21

@author: kot
'''
import env

class TickEvent(object):
    
    def __init__(self, epoch, bid, ask, digit,o=0, h=0, l=0, c=0, v=0):
        self.type = env.EVETYPE_TICK
        self.time = epoch
        self.bid = bid
        self.ask = ask
        self.digit = digit
        self.o = o
        self.h = h
        self.l = l
        self.c = c
        self.v = v
        

        
        