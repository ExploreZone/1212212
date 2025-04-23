import logging
from pathlib import Path

# 测试网配置
BINANCE_TESTNET = True
BINANCE_API_KEY = '15e02d7df4d3d3e550e82d954b097f2f4bf5a068fdfdf7f0492e5823ad0c9a55'
BINANCE_SECRET_KEY = 'e831b485fb1f0862b755138993d0a31f0e870754cdb4e6c473a00a7d939e043b'
API_BASE_URL = 'https://testnet.binancefuture.com'

# 交易参数
SYMBOL = 'BTCUSDT'
LEVERAGE = 15
PER_TRADE_MARGIN = 12.0  # USDT
DAILY_TARGET = 10.0      # USDT

# 技术指标参数
EMA_SHORT = 5
EMA_LONG = 15
ATR_PERIOD = 14
RSI_PERIOD = 14

# 风险参数
MAX_DAILY_LOSS = 30.0    # USDT
STOP_LOSS_PCT = 0.003    # 0.3%
TAKE_PROFIT_PCT = 0.005  # 0.5%

# 日志配置
LOG_DIR = Path(__file__).parent / 'logs'
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('FuturesBot')