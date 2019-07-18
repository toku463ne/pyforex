import math
import lib
import env

import copy
import numpy as np

def getUnitSecs(period):
    t = period[:1]
    i = period[1:]
    
    unit_secs = 0
    if t.upper() == "S":
        unit_secs = int(i)
    elif t.upper() == "M" and i != "":
        unit_secs = int(i)*60
    elif t.upper() == "H": 
        unit_secs = int(i)*60*60
    elif t.upper() == "D":
        unit_secs = 60*60*24
    elif t.upper() == "W": 
        unit_secs = 60*60*24*7
    elif t.upper() == "M": 
        unit_secs = 60*60*24
    if unit_secs == 0: raise Exception("Not proper period type.")
    return unit_secs

def getDecimalPlace(instrument):
    if instrument == "USD_JPY":
        return 2

def calPips(price, instrument="USD_JPY"):
    return price*(10**getDecimalPlace(instrument))

def pip2Price(pip, instrument="USD_JPY"):
    return pip/(10**getDecimalPlace(instrument))

def getFormatString(instrument="USD_JPY"):
    if instrument == "USD_JPY":
        return ".3f"

def getNearEpoch(period, ep):
    u = getUnitSecs(period)
    return math.floor(ep - ep % u)
    

def runDefaultBacktest(instrument, startep, endep, strategy):
    from ticker.backtest import BackTestTicker
    from executor.backtester import BacktestExecutor
    from trading import Trading
    #startep = lib.str2epoch(startstr, env.DATE_FORMAT_NORMAL)
    #endep = lib.str2epoch(endstr, env.DATE_FORMAT_NORMAL)
    ticker = BackTestTicker(instrument, "M5", 
                            startep, endep, spread=0.4)
    executor = BacktestExecutor()
    trading = Trading()
    portfolio, plotelements = trading.run(ticker, executor, strategy)
    return portfolio, plotelements

def runDefaultCandleTrading(instrument, strategy):
    from ticker.latestcandle import LastCandleTicker
    from executor.oanda import OandaExecutor
    from trading import Trading
    ticker = LastCandleTicker(instrument)
    executor = OandaExecutor()
    trading = Trading()
    portfolio, plotelements = trading.run(ticker, executor, strategy)
    return portfolio, plotelements 

def getDensity(hl, ll, cl):
    if len(ll) != len(hl) or len(ll) != len(cl):
        return (False, -1)
    hn = np.array(hl)
    ln = np.array(ll)
    vl = copy.deepcopy(cl)
    vl.extend(hl)
    vl.extend(ll)
    vn = np.array(vl)
    vm = vn.mean()
    hln = (hn-ln)
    hls = hln.std()
    vns = vn.std()
    if vns == 0:
        return 1,vm,hls
    else:
        if (cl[-1]-vm)/vns > 1:
            return 0, -1,-1
        hl_vn_rate = hls/vns
        return hl_vn_rate,vm,hls

def getNearestRoundN(price, instrument="USD_JPY"):
    if instrument == "USD_JPY" or \
        instrument == "GBP_JPY":
        upper = math.ceil(price)
        downer = math.floor(price)
        
    return (upper, downer)