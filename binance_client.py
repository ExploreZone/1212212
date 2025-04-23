from binance.client import Client
from config import BINANCE_API_KEY, BINANCE_SECRET_KEY, API_BASE_URL


class BinanceFuturesTestnet(Client):
    """币安合约测试网专用客户端"""

    def __init__(self):
        super().__init__(
            api_key=BINANCE_API_KEY,
            api_secret=BINANCE_SECRET_KEY,
            requests_params={'timeout': 15}
        )
        self.FUTURES_URL = f"{API_BASE_URL}/fapi/v1"
        self.FUTURES_DATA_URL = f"{API_BASE_URL}/fapi/v1"

    def get_account_balance(self):
        """获取USDT可用余额"""
        acc = self.futures_account()
        return next(
            float(asset['availableBalance'])
            for asset in acc['assets']
            if asset['asset'] == 'USDT'
        )

    def get_current_price(self):
        """获取最新标记价格"""
        return float(self.futures_mark_price(symbol=SYMBOL)['markPrice'])