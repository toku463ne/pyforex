import os
import yaml

conf_path = "C:/Users/kot/Documents/pyforex.yml"
DATE_FORMAT_DEFAULT = "%Y%m%dT%H%M%S"
DATE_FORMAT_NORMAL = "%Y-%m-%dT%H:%M:%S"


MODE_BACKTESTING = 1
MODE_REAL = 2
MODE_QA = 3
MODE_UNITTEST = 4

LOGLEVEL_DEBUG = 1
LOGLEVEL_INFO = 2
LOGLEVEL_ERROR = 3

ORDER_MARKET = 1
ORDER_LIMIT = 2
ORDER_STOP = 3
ORDER_STOPLOSS = 4
ORDER_TAKEPROFIT = 5
ORDER_CLOSE = 6
ORDER_CANCELL = 7

EVETYPE_TICK = 1
EVETYPE_ORDER = 2
EVETYPE_SIGNAL = 3
ESIGNAL_ORDER_FILLED = 1
ESIGNAL_ORDER_CANCELLED = 2
ESIGNAL_TRADE_STARTED = 3
ESIGNAL_TRADE_CLOSED = 4
ESIGNAL_TRADE_CANCELLED = 5

ESTATUS_ORDER_OPENED = 1
ESTATUS_ORDER_CLOSED = 2
ESTATUS_ORDER_CANCELLED = 3
ESTATUS_TRADE_OPENED = 4
ESTATUS_TRADE_ONGOING = 5
ESTATUS_TRADE_CLOSE_REQUESTED = 6
ESTATUS_TRADE_CLOSED = 7
ESTATUS_TRADE_CANCELLED = 8

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
