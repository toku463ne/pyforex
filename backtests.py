'''
Created on 2019/04/22

@author: kot
'''
import lib.tradelib as tradelib
import env
import lib

def runSimple(instrument, startstr, endstr):
    from strategy.simple import SimpleStrategy
    strategy = SimpleStrategy(instrument, profitpips=5)
    startep = lib.str2epoch(startstr, env.DATE_FORMAT_NORMAL)
    endep = lib.str2epoch(endstr, env.DATE_FORMAT_NORMAL)
    portfolio, plotelements  = tradelib.runDefaultBacktest(instrument, 
                                                           startep, endep, strategy)
    return portfolio, plotelements 


def runSimple2(instrument, startstr, endstr):
    from strategy.simple2 import Simple2Strategy
    startep = lib.str2epoch(startstr, env.DATE_FORMAT_NORMAL)
    endep = lib.str2epoch(endstr, env.DATE_FORMAT_NORMAL)
    strategy = Simple2Strategy(instrument, profitpips=5)
    portfolio, plotelements  = tradelib.runDefaultBacktest(instrument, 
                                                           startep, endep, strategy)
    return portfolio, plotelements  
    
    
def runPeakTrigger(instrument, granularity, startstr, endstr, truncateOld=True):
    from strategy.peaktrigger import PeakTriggerStrategy
    startep = lib.str2epoch(startstr, env.DATE_FORMAT_NORMAL)
    endep = lib.str2epoch(endstr, env.DATE_FORMAT_NORMAL)
    strategy = PeakTriggerStrategy(instrument, granularity, 
                                   startep, endep, truncateOld=truncateOld)
    portfolio, plotelements = tradelib.runDefaultBacktest(instrument, 
                                                           startep, endep, strategy)
    return portfolio, plotelements


def runDollCost(instrument, startstr, endstr):
    from strategy.dollcost import DollCostStrategy
    startep = lib.str2epoch(startstr, env.DATE_FORMAT_NORMAL)
    endep = lib.str2epoch(endstr, env.DATE_FORMAT_NORMAL)
    strategy = DollCostStrategy(instrument)
    portfolio, plotelements  = tradelib.runDefaultBacktest(instrument, 
                                                           startep, endep, strategy)
    return portfolio, plotelements
    

def runSlope(instrument, granularity, startstr, 
                 endstr="", ema_span=20, profitpips=5,
                 cachesize=5,
                 peak_span=6,
                 parent_peak_span=3,
                 parent_granularity="D",
                 dens_anal_span=5,
                 maxoldbars=12*24,truncateOld=True):
    from strategy.slope import SlopeStrategy
    startep = lib.str2epoch(startstr, env.DATE_FORMAT_NORMAL)
    if endstr != "":
        endep = lib.str2epoch(endstr, env.DATE_FORMAT_NORMAL)
    else:
        endep = -1
    strategy = SlopeStrategy(instrument, granularity, startep, 
                 endep=endep, ema_span=ema_span, profitpips=profitpips,
                 cachesize=cachesize,
                 peak_span=peak_span,
                 parent_peak_span=parent_peak_span,
                 parent_granularity=parent_granularity,
                 dens_anal_span=dens_anal_span,
                 maxoldbars=maxoldbars,truncateOld=truncateOld)
    portfolio, plotelements  = tradelib.runDefaultBacktest(instrument, 
                                                           startep, endep, strategy)
    return portfolio, plotelements
    



if __name__ == "__main__":
    #runSimple2("USD_JPY", "2019-04-02T09:00:00", "2019-04-02T18:00:00")
    po, pe = runSlope("USD_JPY", "H1", "2019-04-01T00:00:00", 
                      "2019-04-24T00:00:00")
    print(po.getTotalProfit())
