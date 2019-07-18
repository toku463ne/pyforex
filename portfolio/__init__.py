
class Portfolio(object):
    
    def __init__(self, trade_history):
        df = trade_history.getDataFrame()
        self.df = df
    
    def _getGroupBy(self, frequency, sumcols=[]):
        if frequency == "H":
            group_cols = ["year","month","day","hour"]
        elif frequency == "d":
            group_cols = ["year","month","day"]
        elif frequency == "m":
            group_cols = ["year","month"]
        
        df = self.df
        for col in group_cols:
            if col == "year":
                df[col] = df.start_time.dt.year
            if col == "month":
                df[col] = df.start_time.dt.month
            if col == "day":
                df[col] = df.start_time.dt.day
            if col == "hour":
                df[col] = df.start_time.dt.hour
        
        sumcols.extend(group_cols)
        return self.df[sumcols].groupby(group_cols)
        
    def getSum(self, frequency="H"):
        return self._getGroupBy(frequency, ["profit"]).sum()
        
    def getTotalProfit(self):
        if len(self.df) == 0:
            return 0
        return self.df.profit.sum()
                