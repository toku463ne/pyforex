'''
Created on 2019/08/09

@author: kot
'''

def getWhereFromList(wherelist):
    if len(wherelist) == 0:
        return ""
    wherestr = ""
    for w in wherelist:
        if wherestr == "":
            wherestr = w
        else:
            wherestr += " AND " + w
    return "WHERE " + wherestr
