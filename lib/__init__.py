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
    d = datetime.datetime(*time.gmtime(epoch)[:6])
    d = pytz.utc.localize(d)
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
    return dt2epoch(datetime.datetime.now())

def list2str(list, sep=",", enquote=False):
    s = ""
    for v in list:
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


def compFloatList(list1, list2, formatstr="%.3f"):
    if len(list1) != len(list2):
        return False
    for i in range(len(list1)):
        if formatstr.format(list1[i]) != formatstr.format(list2[i]):
            return False
    return True


def compWithList(list1, ids, items, item_name, comp_format=""):
    if len(list1) != len(ids):
        return False
    if len(list1) != len(items):
        return False
    _list1 = copy.deepcopy(list1)
    _ids = copy.deepcopy(ids)
    _items = copy.deepcopy(items)
    while len(_ids) > 0:
        _id = _ids.pop()
        item = _items.pop()
        ev = _list1.pop()
        if comp_format == "":
            if ev.__dict__[item_name] != item:
                return False
        else:
            if comp_format.format(ev.__dict__[item_name]) != comp_format.format(item):
                return False
    return True


def compWithEventQueue(eq, ids, items, item_name, comp_format=""):
    if len(eq) != len(ids):
        return False
    if len(eq) != len(items):
        return False
    _eq = copy.deepcopy(eq)
    _ids = copy.deepcopy(ids)
    _items = copy.deepcopy(items)
    while len(_ids) > 0:
        _id = _ids.pop()
        item = _items.pop()
        (__id, ev) = _eq.pop()
        if __id != _id:
            return False
        if comp_format == "":
            if ev.__dict__[item_name] != item:
                return False
        else:
            if comp_format.format(ev.__dict__[item_name]) != comp_format.format(item):
                return False
    return True


def compDateWithEventQueue(eq, ids, datestrs, item_name, 
                           date_format=env.DATE_FORMAT_NORMAL):
    eps = []
    for datestr in datestrs:
        eps.append(str2epoch(datestr, date_format))
    
    return compWithEventQueue(eq, ids, eps, item_name)


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
    

