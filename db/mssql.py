import env
import pyodbc
from db import DB
import lib
import env

class MSSQLDB(DB):
    def __init__(self):
        si = env.conf["mssqldb"]
        driver = si["driver"] # check driver by pyodbc.drivers()
        server = si["server"]
        if env.run_mode == env.MODE_UNITTEST:
            database = si["testdatabase"]
        elif env.run_mode == env.MODE_QA:
            database = si["qadatabase"]
        else:
            database = si["database"]
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
        
        
    def select1rec(self, sql):
        cur = self.execute(sql)
        row = cur.fetchone()
        if row:
            return row
        
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
        
        



if __name__ == "__main__":
    env.run_mode = env.MODE_UNITTEST
    d = MSSQLDB()
    cur = d.execute("select @@version")
    a = cur.fetchall()
    print(a)

    d.execCreateTsql("../templates/create_meta_table.sql", "test_meta")
    

