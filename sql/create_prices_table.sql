IF NOT EXISTS (SELECT * FROM SYSOBJECTS WHERE NAME='#TABLENAME#' AND XTYPE='U')
	CREATE TABLE #TABLENAME# (
	    [EP] INT NOT NULL,
	    [O] FLOAT,
	    [H] FLOAT,
	    [L] FLOAT,
	    [C] FLOAT,
	    [V] INT,
	    CONSTRAINT PK_#TABLENAME#_EPOCH PRIMARY KEY CLUSTERED ([EP])
	);