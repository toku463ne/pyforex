'''
Created on 2019/04/10

@author: kot
'''
import env

def getPriceTable(instrument, granularity):
    return "%s_%s_prices" % (instrument, granularity)

def getMetainfTable(instrument, granularity):
    return "%s_%s_metainf" % (instrument, granularity)

def getOrderHistoryTable(transaction_name):
    return "%s_orderh" % (transaction_name)

def getTradeHistoryTable(transaction_name):
    return "%s_tradeh" % (transaction_name)

def getTransactionSequence(transaction_name):
    return "%s_transaction_seq" % (transaction_name)

def getDataGetterName(instrument, granularity):
    return "%s_%s" %  (instrument, granularity)

def getOandaTrandactionIDTableName():
    return "oanda_transaction_id"

def getDBKey():
    if env.run_mode == env.MODE_UNITTEST:
        dbkey = "testdatabase"
    elif env.run_mode == env.MODE_QA:
        dbkey = "qadatabase"
    else:
        dbkey = "database"
    return dbkey
