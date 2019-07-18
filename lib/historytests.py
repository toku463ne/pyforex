'''
Created on 2019/04/27

@author: kot
'''

def compWithEventQueue(eq, ids, items, item_name):
    if len(eq) != len(ids):
        return False
    if len(eq) != len(items):
        return False
    while len(ids) > 0:
        _id = ids.pop()
        item = items.pop()
        (__id, ev) = eq.pop()
        if __id != _id:
            return False
        if ev.__dict__[item_name] != item:
            return False
    return True

