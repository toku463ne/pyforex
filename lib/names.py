'''
Created on 2019/04/10

@author: kot
'''

def getPriceTable(instrument, granularity):
    return "%s_%s_prices" % (instrument, granularity)

def getMetainfTable(instrument, granularity):
    return "%s_%s_metainf" % (instrument, granularity)

def getDataGetterName(instrument, granularity):
    return "%s_%s" %  (instrument, granularity)
