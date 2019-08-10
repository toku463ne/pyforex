'''
Created on 2019/08/08

@author: kot
'''
import lib
import env

import copy

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
        eps.append(lib.str2epoch(datestr, date_format))
    
    return compWithEventQueue(eq, ids, eps, item_name)

