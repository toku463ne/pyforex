'''
Created on 2019/04/21

@author: kot
'''
import env

class SignalEvent(object):
    def __init__(self, _id, signal):
        self.id = _id
        self.type = env.EVETYPE_SIGNAL
        self.signal = signal
        