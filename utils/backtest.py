import pandas as pd

def backtest_strategy(df, signals, sl_pct=1.5, tp_pct=5.0):
    trades = []
    equity = [10000]  # Starting equity
    balance = equity[0]

    for _, signal in signals.iterrows():
        entry_price = signal["Entry Price"]
        direction = signal["Direction"]
        entry_time = signal["Time"]

        if direction == "Buy":
            sl = entry_price * (1 - sl_pct / 100)
            tp = entry_price * (1 + tp_pct / 100)
            prices = df.loc[entry_time:].copy()
            for time, row in prices.iterrows():
                if row["Low"] <= sl:
                    result = "Loss"
                    exit_price = sl
                    break
                elif row["High"] >= tp:
                    result = "Win"
                    exit_price = tp
                    break
            else:
                result = "Open"
                exit_price = prices.iloc[-1]["Close"]

        elif direction == "Sell":
            sl = entry_price * (1 + sl_pct / 100)
            tp = entry_price * (1 - tp_pct / 100)
            prices = df.loc[entry_time:].copy()
            for time, row in prices.iterrows():
                if row["High"] >= sl:
                    result = "Loss"
                    exit_price = sl
                    break
                elif row["Low"] <= tp:
                    result = "Win"
                    exit_price = tp
                    break
            else:
                result = "Open"
                exit_price = prices.iloc[-1]["Close"]

        pnl_pct = ((exit_price - entry_price) / entry_price) * 100
        if direction == "Sell":
            pnl_pct *= -1

        balance *= 1 + (pnl_pct / 100)
        equity.append(balance)

        trades.append({
            "Time": entry_time,
            "Direction": direction,
            "Entry Price": entry_price,
            "Exit Price": exit_price,
            "Result": result,
            "PnL %": pnl_pct,
        })

    return pd.DataFrame(trades), equity
