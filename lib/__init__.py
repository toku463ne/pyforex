import sys
import os
import datetime
import time
import calendar
import pytz
import math
import importlib
import inspect
import yaml
import env
import copy


def printDebug(ep, msg):
    if env.loglevel <= env.LOGLEVEL_DEBUG:
        printMsg(ep, "DEBUG | %s" % msg)
        
def printInfo(ep, msg):
    if env.loglevel <= env.LOGLEVEL_INFO:
        printMsg(ep, "INFO  | %s" % msg)

def printError(ep, msg):
    if env.loglevel <= env.LOGLEVEL_ERROR:
        printMsg(ep, "ERROR | %s" % msg)

def printMsg(ep, msg):
    print("%s | %s" % (epoch2str(ep, env.DATE_FORMAT_NORMAL), msg))
   
def log(msg):
    now = datetime.datetime.now()
    t = now.strftime(env.DATE_FORMAT_NORMAL)
    msg = "%s | %s" % (t, str(msg))
    print(msg)
    
def epoch2dt(epoch):
    #d = datetime.datetime(*time.gmtime(epoch)[:6])
    d = datetime.datetime.utcfromtimestamp(epoch)
    #d = pytz.utc.localize(d)
    return d

def dt2epoch(gmdt):
    return int(calendar.timegm(gmdt.timetuple()))

def str2dt(strgmdt, format=env.DATE_FORMAT_NORMAL):
    d = datetime.datetime.strptime(strgmdt, format)
    d = pytz.utc.localize(d)
    return d
    
def str2epoch(strgmdt, format=env.DATE_FORMAT_NORMAL):
    return dt2epoch(str2dt(strgmdt, format))
    
def dt2str(gmdt, format=env.DATE_FORMAT_NORMAL):
    return gmdt.strftime(format)

def epoch2str(epoch, format=env.DATE_FORMAT_NORMAL):
    return dt2str(epoch2dt(epoch), format)

def nowepoch():
    return time.time()

def list2str(list1, sep=",", enquote=False):
    s = ""
    for v in list1:
        if enquote:
            v = "'%s'" % str(v)
        if s == "":
            s = v
        else:
            s = "%s%s %s" % (s, sep, str(v))
    return s

def addPrefix2List(prefix, l):
    _l = []
    for i in l:
        _l.append("%s%s" % (str(prefix),str(i)))
    return _l

def load_yaml(y):
    return yaml.load(open(y), Loader=yaml.FullLoader)



def getRateList(n_blocks, n_digits):
    n_blocks = int(n_blocks)
    n_digits = int(n_digits)
    nList = []
    if n_blocks == 0:
        return [(0,)*n_digits]
    if n_digits == 1:
        return [(n_blocks,)]
    for b in reversed(range(n_blocks+1)):
        res = getRateList(n_blocks-b, n_digits-1)
        for r in res:
            r += (b,)
            nList.append(r)
    return nList

def truncFromDecimalPlace(f, d):
    return math.floor(f*(10**d))/(10**d)


if __name__ == "__main__":
    a = getRateList(5, 3)
    print(a)
    

