import env
from trading.trader import Trader
import lib
from portfolio import Portfolio
from collections import deque
import pandas as pd
import strategy
from plotelement.tradehist import PlotEleTradeHist
import time
import signal



class Trading(object):
    
    def run(self, ticker, executor, strategy, transaction):
        last_time = time.time()
        events = deque()
        tran = transaction
        
        def signal_handler(self, signum, frame):
            print("received %d" % (signum))
            tran.flush()
            print("finishing program")
            exit(0)
    
        
        strategy.events = events
        strategy.tran = tran
        executor.queue = events
        executor.tran = tran
        oldevent = None
        has_tick = False
        cnt_from_last_flush = 0
        signal.signal(signal.SIGINT, signal_handler)
        while True:
            if has_tick == False:
                event = ticker.tick()
                if event == None:
                    break
                if oldevent == None:
                    if event.type == env.EVETYPE_TICK:
                        lib.printInfo(event.time, "starting")
                #lib.printDebug(event.time, "tick")
                events.appendleft(event)
                has_tick = True
            
            event = events.pop()
            if event.type == env.EVETYPE_TICK:
                has_tick = False
            
            if event.type in [env.EVETYPE_SIGNAL, env.EVETYPE_TICK]:
                strategy._run(event)
                
            if event.type in [env.EVETYPE_TICK, env.EVETYPE_ORDER]:
                executor._run(event)
            if event.type == env.EVETYPE_TICK:
                oldevent = event
            
                cur_time = time.time()
                if cur_time - last_time >= env.TRADING_HISTORY_FLUSH_INTERVAL or \
                    cnt_from_last_flush >= env.TRADING_HISTORY_FLUSH_INTERVAL:
                    last_time = cur_time
                    cnt_from_last_flush = 0
                    tran.flush()
                    lib.printInfo(event.time, "Trading | Flushed transaction history.")
                else:
                    cnt_from_last_flush += 1
        lib.printInfo(oldevent.time, "finished")
        
        
        
        #order_history = tran.order_hqueue
        #trade_history = tran.trade_hqueue
        tran.flush()
        plotelements = strategy.getPlotElements()
        portofolio = tran.getPortofolio()
        return portofolio, plotelements
        
        #plotelements.append(PlotEleTradeHist(trade_history))
        #return order_history, trade_history, plotelements 
        #return plotelements
        