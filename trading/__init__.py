'''
Created on 2019/11/15

@author: kot
'''
import env
import lib
from collections import deque
import time
import signal

def run(ticker, executor, strategy, manager, flushHist=True):
    order_events = []
    executor.manager = manager
    strategy.manager = manager
    cnt = 0
    
    while True:
        tick_event = ticker.tick()
        if tick_event == None:
            if ticker.ticker_type == env.TICKTYPE_OFFLINE:
                break
            time.sleep(1)
            continue
        
        while len(order_events) > 0:
            executor.receiveOrder(order_events.pop(0))
        
        signal_events = executor.onTick(tick_event)
        
        while len(signal_events) > 0:
            strategy.onSignal(signal_events.pop(0))
        
        order_events = strategy.onTick(tick_event)
        
        cnt += 1
        if cnt >= env.TRADING_HISTORY_FLUSH_INTERVAL:
            cnt = 0
            if flushHist:
                manager.flushHistory()
        

    return manager.history