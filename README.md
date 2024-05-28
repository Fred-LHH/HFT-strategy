# HFT-strategy
This strategy is based on constructing intraday factors from 3-second snapshot data and uses a random forest model for high-frequency intraday trading.
**precondition:**
Test on a single asset: Initially hold 5 million CNY worth of a particular stock. Calculate daily PnL as intraday trading profit divided by 5 million CNY. The number of shares bought and sold within the day must be equal, and there is no requirement on the order of buying and selling. The number of shares bought within the day must be less than or equal to the initial number of shares held.
Fees:
A stamp duty rate of 0.05% is charged on sales.
A commission rate of 0.01% is charged on both buys and sells.

The current limitations are as follows:

1.The backtesting framework is not sufficiently comprehensive, as it does not consider stop-loss and take-profit mechanisms.
2.High-frequency factors have not been thoroughly explored.
3.The model is relatively simplistic.
4.The selection of hyperparameters.

对单只股票进行测试，使用日内3s快照数据构建因子进行日内交易.期初持有500w市值股票.每天的买入=卖出
手续费0.01%
印花税0.05%
