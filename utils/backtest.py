import pandas as pd

def backtest_strategy(df, signals, sl_pct, tp_pct):
    trades = []
    equity = [10000]  # Starting equity
    balance = equity[0]

    for _, signal in signals.iterrows():
        entry_price = signal["price"]
        entry_time = signal["datetime"]
        direction = signal["signal"]

        if direction == "breakout_long":
            sl = entry_price * (1 - sl_pct / 100)
            tp = entry_price * (1 + tp_pct / 100)
        elif direction == "breakout_short":
            sl = entry_price * (1 + sl_pct / 100)
            tp = entry_price * (1 - tp_pct / 100)
        else:
            continue

        # Find exit
        df_slice = df[df["datetime"] > entry_time]
        exit_price = None
        exit_time = None
        for _, row in df_slice.iterrows():
            high = row["High"]
            low = row["Low"]
            if direction == "breakout_long":
                if low <= sl:
                    exit_price = sl
                    exit_time = row["datetime"]
                    break
                elif high >= tp:
                    exit_price = tp
                    exit_time = row["datetime"]
                    break
            elif direction == "breakout_short":
                if high >= sl:
                    exit_price = sl
                    exit_time = row["datetime"]
                    break
                elif low <= tp:
                    exit_price = tp
                    exit_time = row["datetime"]
                    break

        if exit_price is not None:
            pnl = (exit_price - entry_price) if direction == "breakout_long" else (entry_price - exit_price)
            trades.append({
                "entry_time": entry_time,
                "entry_price": entry_price,
                "exit_time": exit_time,
                "exit_price": exit_price,
                "direction": direction,
                "pnl": pnl
            })
            balance += pnl
            equity.append(balance)

    return pd.DataFrame(trades), equity
