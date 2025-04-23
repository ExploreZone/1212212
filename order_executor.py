from binance.enums import *
from config import (
    logger, SYMBOL, LEVERAGE,
    PER_TRADE_MARGIN, STOP_LOSS_PCT, TAKE_PROFIT_PCT
)
from binance_client import BinanceFuturesTestnet


class OrderExecutor:
    def __init__(self):
        self.client = BinanceFuturesTestnet()
        self.logger = logger.getChild('Order')

    def _calc_position_size(self, price):
        """计算合约数量"""
        try:
            # 获取合约规格
            info = self.client.futures_exchange_info()
            symbol_info = next(s for s in info['symbols'] if s['symbol'] == SYMBOL)
            lot_size = [f for f in symbol_info['filters'] if f['filterType'] == 'LOT_SIZE'][0]

            # 计算数量
            quantity = PER_TRADE_MARGIN * LEVERAGE / price
            quantity = round(quantity, int(lot_size['stepSize'].find('1') - 1))
            return str(quantity)
        except Exception as e:
            self.logger.error(f"计算数量失败: {str(e)}")
            return None

    def execute_trade(self, signal):
        """执行交易"""
        try:
            # 设置杠杆
            self.client.futures_change_leverage(
                symbol=SYMBOL,
                leverage=LEVERAGE
            )

            # 获取当前价格
            price = self.client.get_current_price()

            # 计算下单量
            qty = self._calc_position_size(price)
            if not qty:
                return False

            # 开仓方向
            side = SIDE_BUY if signal == 'LONG' else SIDE_SELL

            # 市价单开仓
            order = self.client.futures_create_order(
                symbol=SYMBOL,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=qty
            )
            self.logger.info(f"开仓成功 | 方向:{signal} | 数量:{qty} | 价格:{price:.2f}")

            # 设置止损止盈
            self._place_stop_order(signal, price)
            return True
        except Exception as e:
            self.logger.error(f"下单失败: {str(e)}")
            return False

    def _place_stop_order(self, signal, entry_price):
        """设置止损单"""
        try:
            stop_price = round(
                entry_price * (1 - STOP_LOSS_PCT) if signal == 'LONG'
                else entry_price * (1 + STOP_LOSS_PCT),
                2
            )

            self.client.futures_create_order(
                symbol=SYMBOL,
                side=SIDE_SELL if signal == 'LONG' else SIDE_BUY,
                type=FUTURE_ORDER_TYPE_STOP_MARKET,
                stopPrice=stop_price,
                closePosition='true',  # 测试网特殊要求
                priceProtect='true'
            )
            self.logger.info(f"止损单设置 | 触发价:{stop_price:.2f}")
        except Exception as e:
            self.logger.error(f"止损单设置失败: {str(e)}")