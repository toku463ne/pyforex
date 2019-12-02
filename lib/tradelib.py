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

def getSpread(instrument):
    if instrument == "USD_JPY":
        return 0.4

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
    

def getNearestRoundN(price, instrument="USD_JPY"):
    if instrument == "USD_JPY" or \
        instrument == "GBP_JPY":
        upper = math.ceil(price)
        downer = math.floor(price)
        
    return (upper, downer)