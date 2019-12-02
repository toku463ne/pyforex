'''
Created on 2019/11/26

@author: kot
'''

from index import TechnicalIndex
import lib


class StdIndex(TechnicalIndex):
    def __init__(self, subChart, span):
        super(StdIndex, self).__init__("StdIndex%d" % span, 
                                        subChart.instrument, 
                                        subChart.granularity)
        
        
