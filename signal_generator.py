import talib
import numpy as np
from config import logger, SYMBOL, EMA_SHORT, EMA_LONG, ATR_PERIOD, RSI_PERIOD
from binance_client import BinanceFuturesTestnet


class SignalGenerator:
    def __init__(self):
        self.client = BinanceFuturesTestnet()
        self.logger = logger.getChild('Signal')

    def _get_klines(self):
        """获取5分钟K线数据"""
        try:
            klines = self.client.futures_klines(
                symbol=SYMBOL,
                interval=Client.KLINE_INTERVAL_5MINUTE,
                limit=50
            )
            return [{
                'open': float(k[1]),
                'high': float(k[2]),
                'low': float(k[3]),
                'close': float(k[4]),
                'volume': float(k[5])
            } for k in klines]
        except Exception as e:
            self.logger.error(f"获取K线失败: {str(e)}")
            return None

    def generate_signal(self):
        """生成交易信号"""
        try:
            klines = self._get_klines()
            if not klines or len(klines) < 20:
                return 'NEUTRAL'

            closes = np.array([k['close'] for k in klines])
            highs = np.array([k['high'] for k in klines])
            lows = np.array([k['low'] for k in klines])

            # 计算指标
            ema_short = talib.EMA(closes, timeperiod=EMA_SHORT)[-1]
            ema_long = talib.EMA(closes, timeperiod=EMA_LONG)[-1]
            atr = talib.ATR(highs, lows, closes, timeperiod=ATR_PERIOD)[-1]
            rsi = talib.RSI(closes, timeperiod=RSI_PERIOD)[-1]

            # 生成信号
            if ema_short > ema_long and rsi < 35:
                self.logger.info(
                    f"LONG信号: EMA({EMA_SHORT})={ema_short:.2f} > EMA({EMA_LONG})={ema_long:.2f}, RSI={rsi:.1f}")
                return 'LONG'
            elif ema_short < ema_long and rsi > 65:
                self.logger.info(
                    f"SHORT信号: EMA({EMA_SHORT})={ema_short:.2f} < EMA({EMA_LONG})={ema_long:.2f}, RSI={rsi:.1f}")
                return 'SHORT'
            else:
                return 'NEUTRAL'
        except Exception as e:
            self.logger.error(f"信号生成异常: {str(e)}")
            return 'NEUTRAL'