'''
Created on 2019/08/08

@author: kot
'''
from transaction import Transaction
from portfolio.mssql import MSSQLPortfolio
from db.mssql import MSSQLDB
import env
import lib.names as names
import lib

class MSSQLTransaction(Transaction):
    def __init__(self, name):
        super(MSSQLTransaction, self).__init__(name)
        self.db = MSSQLDB()
        self.seqname = names.getTransactionSequence(name)
        self.orderhT = names.getOrderHistoryTable(name)
        self.tranhT = names.getTradeHistoryTable(name)
        self.db.createSequence(self.seqname)
        self.db.createTable(self.orderhT, "orderhistory")
        self.db.createTable(self.tranhT, "tradehistory")
        if env.run_mode in [env.MODE_BACKTESTING, 
                            env.MODE_SIMULATE, env.MODE_UNITTEST]:
            self.db.truncateTable(self.orderhT)
            self.db.truncateTable(self.tranhT)
            self.db.restartSeq(self.seqname)
        
    def genID(self):
        return self.db.nextSeq(self.seqname)
    
    def getPortofolio(self):
        return MSSQLPortfolio(self.name)
        
    
    def flushOrderHistory(self):
        while True:
            (_id, oh) = self.order_hqueue.pop()
            if _id == -1:
                break
            sql = "insert into %s values(\
            ?,?,?,?,?,?,?,?,?,?,?,?,?,?);" % self.orderhT 
            self.db.execute(sql, 
               (oh.id, #[ID] INT NOT NULL,
               oh.order_id, # [ORDER_ID] INT,
               oh.startep, # [STARTEP] INT,
               oh.validep, # [VALIDEP] INT,
               lib.epoch2dt(oh.startep),
               lib.epoch2dt(oh.validep),
               oh.instrument, #[INSTRUMENT] char(7),
               oh.side,
               oh.order_type,
               oh.units,
               oh.price,
               oh.takeprofit_price,
               oh.stoploss_price,
               oh.desc)
               )
            
    
    '''
        [STARTDT] INT,
        [VALIDDT] INT,
        [INSTRUMENT] char(7),
        [SIDE] INT,
        [ORDER_TYPE] varchar(20),
        [UNITS] INT,
        [PRICE] FLOAT,
        [TAKEPROFIT_PRICE] FLOAT,
        [STOPLOSS_PRICE] FLOAT,
        [DESC] VARCHAR(100),
 
    '''

    
    def flushTradeHistory(self):
        while True:
            (_id, oh) = self.trade_hqueue.pop()
            if _id == -1:
                break
            sql = "insert into %s values(\
            ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);" % self.tranhT 
            self.db.execute(sql, 
               (oh.id, #[ID] INT NOT NULL,
               oh.trade_id, #[TRADE_ID] INT,
               oh.startep, #[STARTEP] INT,
               oh.endep, #[ENDEP] INT,
               lib.epoch2dt(oh.startep), #[STARTDT] datetime,
               lib.epoch2dt(oh.endep), #[ENDDT] datetime,
               oh.instrument, #[INSTRUMENT] char(7),
               oh.side, #[SIDE] INT,
               oh.units, #[UNITS] INT,
               oh.start_price,
               oh.end_price,
               oh.profit,
               oh.takeprofit_price,
               oh.stoploss_price,
               oh.desc)
               )
    
    '''
        [START_PRICE] FLOAT,
        [END_PRICE] FLOAT,
        [PROFIT] FLOAT,
        [TAKEPROFIT_PRICE] FLOAT,
        [STOPLOSS_PRICE] FLOAT,
        [DESC] VARCHAR(100),

        '''