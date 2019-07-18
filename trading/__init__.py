import env
from trading.trader import Trader
from trading.transaction import Transaction
import lib
from portfolio import Portfolio

from collections import deque
import pandas as pd
import strategy
from plotelement.tradehist import PlotEleTradeHist

class Trading(object):
    
            
    def run(self, ticker, executor, strategy):
        events = deque()
        tran = Transaction()
        strategy.events = events
        strategy.tran = tran
        executor.queue = events
        executor.tran = tran
        oldevent = None
        has_tick = False
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
        lib.printInfo(oldevent.time, "finished")
        #order_history = tran.order_hqueue
        trade_history = tran.trade_hqueue
        
        #if len(trade_history) > 0:
        #    df = trade_history.getDataFrame()
        #    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        #        print(df[["profit", "side", "units",
        #              "start_price", "end_price",
        #              "start_time", "end_time",
        #              "desc"]])
        
        plotelements = strategy.getPlotElements()
        plotelements.append(PlotEleTradeHist(trade_history))
        #return order_history, trade_history, plotelements 
        return Portfolio(trade_history),plotelements
        