import os
import yaml

conf_path = "C:/Users/kot/Documents/pyforex.yml"
DATE_FORMAT_DEFAULT = "%Y%m%dT%H%M%S"
DATE_FORMAT_NORMAL = "%Y-%m-%dT%H:%M:%S"
DATE_FORMAT_NORMAL2 = "%Y-%m-%d %H:%M:%S"

MODE_BACKTESTING = 1 #Test by loading history data in advance. Fastest.
MODE_REAL = 2 # Real
MODE_QA = 3 # Test with real time data using test account with virtual budget
MODE_UNITTEST = 4 # Use lab database and break the database before testing
MODE_SIMULATE = 5 # Test with history data but getting tick data every time.

LOGLEVEL_DEBUG = 1
LOGLEVEL_INFO = 2
LOGLEVEL_ERROR = 3

CMD_CREATE_MARKET_ORDER = 1
CMD_CREATE_LIMIT_ORDER = 2
CMD_CREATE_STOP_ORDER = 3
CMD_CANCEL = 4

ORDERTYPE_ORDER = 1
ORDERTYPE_TRADE = 2

EVETYPE_TICK = 1
EVETYPE_ORDER = 2
EVETYPE_SIGNAL = 3


ESTATUS_NONE = 0
ESTATUS_ORDER_OPENED = 1
ESTATUS_ORDER_CLOSED = 2
ESTATUS_TRADE_OPENED = 3
ESTATUS_TRADE_CLOSED = 4


TICKTYPE_ONLINE = 1
TICKTYPE_OFFLINE = 2


TRADING_HISTORY_FLUSH_INTERVAL = 60*60 #move history events to db every hours

SIDE_BUY = 1
SIDE_SELL = -1

CHART_NBARS_PER_CHART = 120

order_header = ["id", "order_id", 
                "instrument", "side", "order_type", "units", 
                "price", "takeprofit_price", "stoploss_price",
                "start_time", "valid_time", "end_time", "desc"]

trade_header = ["id", "trade_id",  
                "instrument", "side", "units", "start_price", "end_price", "profit",
                "start_time", "end_time", "desc"]

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SQL_DIR = '%s/%s' % (BASE_DIR, "sql")

conf = yaml.load(open(conf_path), Loader=yaml.FullLoader)

dataGetters = {}
loglevel = conf["loglevel"]
run_mode = conf["run_mode"]
