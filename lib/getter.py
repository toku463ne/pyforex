'''
Created on 2019/04/14

@author: kot
'''
import env
import lib.names

def launchDataGetter(instrument, granularity):
    name = lib.names.getDataGetterName(instrument, granularity)
    if name in env.dataGetters.keys():
        dg = env.dataGetters[name]
    else:    
        datagetter_type = env.conf["datagetter_type"]
        if datagetter_type == "mssqloanda":
            from data_getter.mssql import MSSQLGetter
            from data_getter.oanda import OandaGetter
            dg = MSSQLGetter(OandaGetter(instrument, granularity))
            env.dataGetters[name] = dg
        '''
        Add here more data getters
        '''
    return dg
    
    
def dropDataGetter(instrument, granularity):
    name = lib.names.getDataGetterName(instrument, granularity)
    if name in env.dataGetters.keys():
        del env.dataGetters[name]
        
        
def getPrices(instrument, granularity, startep, endep):
    name = lib.names.getDataGetterName(instrument, granularity)
    if name in env.dataGetters.keys():
        dg = env.dataGetters[name]
    else:
        dg = launchDataGetter(instrument, granularity)
    return dg.getPrice(startep, endep)


def getNPrices(instrument, granularity, endep, nbars):
    name = lib.names.getDataGetterName(instrument, granularity)
    if name in env.dataGetters.keys():
        dg = env.dataGetters[name]
    else:
        dg = launchDataGetter(instrument, granularity)
    return dg.getNPrice(endep, nbars)

def getCurrPrice(instrument, granularity):
    name = lib.names.getDataGetterName(instrument, granularity)
    if name in env.dataGetters.keys():
        dg = env.dataGetters[name]
    else:
        dg = launchDataGetter(instrument, granularity)
    return dg.getCurrPrice()

        
    