import env
import pyodbc
from db import DB
import lib
import lib.names as names
import env
import pandas as pd

class MSSQLDB(DB):
    def __init__(self):
        si = env.conf["mssqldb"]
        driver = si["driver"] # check driver by pyodbc.drivers()
        server = si["server"]
        dbkey = names.getDBKey()
        database = si[dbkey]
        username = si["username"] 
        password = si["password"]
        cstring = 'DRIVER=%s;SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % \
            (driver, server, database, username, password)
        self.connection = pyodbc.connect(cstring, autocommit=True)
        

    def execute(self, sql, params=()):
        try:
            cur = self.connection.cursor()
            return cur.execute(sql, params)
        except Exception as e:
            lib.log("Error at SQL")
            lib.log(sql)
            raise e
        
    def get_df(self, sql):
        df = pd.read_sql(sql, self.connection)
        return df
        
    def truncateTable(self, tablename):
        try:
            cur = self.connection.cursor()
            sql = "truncate table %s;" % tablename
            return cur.execute(sql)
        except Exception as e:
            lib.log("Error at SQL")
            lib.log(sql)
            raise e
        
        
    def select1rec(self, sql):
        cur = self.execute(sql)
        row = cur.fetchone()
        if row:
            return row
        
    
    def nextSeq(self, seqname):
        sql = "select next value for %s;" % seqname
        cur = self.execute(sql)
        row = cur.fetchone()
        if row:
            return row[0]
        
        
    def restartSeq(self, seqname):
        try:
            cur = self.connection.cursor()
            sql = "alter sequence %s restart with 1" % seqname
            return cur.execute(sql)
        except Exception as e:
            lib.log("Error at SQL")
            lib.log(sql)
            raise e
        
        
        
    def countTable(self, tablename, whereList=[]):
        strwhere = ""
        if len(whereList) > 0:
            strwhere = "where %s" % ("and ".join(whereList))
        sql = "select count(*) as cnt from %s %s" % \
            (tablename, strwhere)
        cur = self.execute(sql)
        row = cur.fetchone()
        return row.cnt

    def close(self):
        if self.connection != None:
            self.connection.close()
            
            
    def execCreateTsql(self, sqlfile, tablename):
        try:            
            f = open(sqlfile, "r")
            sql = f.read()
            sql = sql.replace("#TABLENAME#", tablename)
            f.close()
            cur = self.execute(sql)
            return cur
        except:
            raise
        
        
    def createTable(self, tablename, templatename):
        self.execCreateTsql("%s/create_%s_table.sql" % (env.SQL_DIR, 
                                                        templatename), tablename)
        
    def createSequence(self, seqname):
        sqlfile = "%s/create_sequence.sql" % (env.SQL_DIR)
        try:            
            f = open(sqlfile, "r")
            sql = f.read()
            sql = sql.replace("#SEQUENCENAME#", seqname)
            f.close()
            cur = self.execute(sql)
            return cur
        except:
            raise
        


if __name__ == "__main__":
    env.run_mode = env.MODE_UNITTEST
    d = MSSQLDB()
    cur = d.execute("select @@version")
    a = cur.fetchall()
    print(a)

    d.execCreateTsql("../templates/create_meta_table.sql", "test_meta")
    

