'''
Created on 2019/05/26

@author: kot
'''
import lib
import datetime

d = datetime.datetime(2018,10,1,14,30)
e = lib.dt2epoch(d)
print(e)