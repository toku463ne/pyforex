'''
Created on 2019/08/10

@author: kot
'''

import signal
import time

def signal_handler(signum, frame):
    print("received %d %s" % (signum, str(frame)))

signal.signal(signal.SIGINT, signal_handler)

while True:
    time.sleep(1)
    print("next")