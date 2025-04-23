from config import logger, MAX_DAILY_LOSS, STOP_LOSS_PCT, TAKE_PROFIT_PCT


class RiskManager:
    def __init__(self):
        self.daily_pnl = 0.0
        self.consecutive_loss = 0
        self.logger = logger.getChild('Risk')

    def check_risk(self, current_atr):
        """执行风控检查"""
        self._check_daily_loss()
        self._check_consecutive_loss()
        return self._adjust_leverage(current_atr)

    def _check_daily_loss(self):
        if self.daily_pnl <= -MAX_DAILY_LOSS:
            self.logger.critical(f"触发日亏损熔断! 累计亏损:{-self.daily_pnl:.2f} USDT")
            raise RuntimeError("Daily loss limit reached")

    def _check_consecutive_loss(self):
        if self.consecutive_loss >= 3:
            self.logger.critical(f"触发连续亏损熔断! 连续亏损次数:{self.consecutive_loss}")
            raise RuntimeError("Consecutive loss limit reached")

    def _adjust_leverage(self, atr):
        """根据波动率调整杠杆"""
        if atr < 0.002:
            self.logger.warning("低波动市场，杠杆降至10倍")
            return 10
        elif atr > 0.005:
            self.logger.warning("高波动市场，杠杆升至20倍")
            return 20
        return LEVERAGE

    def update_status(self, profit):
        """更新交易状态"""
        self.daily_pnl += profit
        if profit < 0:
            self.consecutive_loss += 1
            self.logger.warning(f"交易亏损: {-profit:.2f} USDT | 连续亏损次数: {self.consecutive_loss}")
        else:
            self.consecutive_loss = 0
            self.logger.info(f"交易盈利: {profit:.2f} USDT | 累计收益: {self.daily_pnl:.2f} USDT")