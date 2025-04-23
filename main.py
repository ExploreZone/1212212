import time
from config import logger, PER_TRADE_MARGIN, TAKE_PROFIT_PCT, DAILY_TARGET, STOP_LOSS_PCT
from signal_generator import SignalGenerator
from risk_manager import RiskManager
from order_executor import OrderExecutor


def main():
    logger.info("=== 币安合约模拟交易启动 ===")

    signal_gen = SignalGenerator()
    risk_mgr = RiskManager()
    executor = OrderExecutor()

    try:
        while True:
            try:
                # 生成交易信号
                signal = signal_gen.generate_signal()

                if signal != 'NEUTRAL':
                    # 执行交易
                    success = executor.execute_trade(signal)

                    if success:
                        # 模拟计算盈利(实际需通过API获取)
                        profit = PER_TRADE_MARGIN * (TAKE_PROFIT_PCT if success else -STOP_LOSS_PCT)
                        risk_mgr.update_status(profit)

                        # 达到日目标后停止
                        if risk_mgr.daily_pnl >= DAILY_TARGET:
                            logger.info(f"达到日盈利目标: {DAILY_TARGET} USDT")
                            break

                # 风控检查
                current_atr = 0.004  # 需实际获取ATR值
                risk_mgr.check_risk(current_atr)

                time.sleep(60)  # 每分钟检查一次

            except KeyboardInterrupt:
                logger.info("用户主动终止策略")
                break
            except Exception as e:
                logger.error(f"主循环异常: {str(e)}")
                time.sleep(300)  # 异常后暂停5分钟

    finally:
        logger.info("=== 模拟交易结束 ===")


if __name__ == "__main__":
    main()