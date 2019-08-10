IF NOT EXISTS (SELECT * FROM SYSOBJECTS WHERE NAME='#TABLENAME#' AND XTYPE='U')
	CREATE TABLE #TABLENAME# (
	    [ID] INT NOT NULL,
	    [TRADE_ID] INT,
	    [STARTEP] INT,
	    [ENDEP] INT,
	    [STARTDT] datetime,
	    [ENDDT] datetime,
	    [INSTRUMENT] char(7),
	    [SIDE] INT,
	    [UNITS] INT,
	    [START_PRICE] FLOAT,
	    [END_PRICE] FLOAT,
	    [PROFIT] FLOAT,
	    [TAKEPROFIT_PRICE] FLOAT,
	    [STOPLOSS_PRICE] FLOAT,
	    [DESC] VARCHAR(100),
	    PRIMARY KEY (ID),
	);
/**
        self.id = _id
        self.order_id = order_id
        self.instrument = instrument
        self.side = side
        self.order_type = order_type
        self.units = units
        self.price = price
        self.status = status
        self.takeprofit_price = takeprofit_price
        self.stoploss_price = stoploss_price
        self.start_time = start_time
        self.valid_time = valid_time
        self.end_time = end_time
        self.desc = desc
        self.trade_id = -1
   **/     