'''
Created on 2019/08/10

@author: kot
'''
import os
import sys
import lib.realtime as app
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

#appname = sys.argv[1]
appname = "simple"

if appname == "simple":
    app.runSimple(localTrading=False)
if appname == "simple2":
    app.runSimple2(localTrading=False)
    
    