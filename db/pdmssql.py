'''
Created on 2019/08/09

@author: kot
'''
from db import DB
import pandas as pd
import env
import lib.names as names
import pymssql


class PDMSSQL(DB):
    
    def __init__(self):
        si = env.conf["mssqldb"]
        server = si["server"]
        dbkey = names.getDBKey()
        database = si[dbkey]
        username = si["username"] 
        password = si["password"]
        self.conn = pymssql.connect(server=server, 
                               user=username, 
                               password=password, 
                               database=database)
        
    def read_sql(self, sql):
        df = pd.read_sql(sql, self.conn)
        return df