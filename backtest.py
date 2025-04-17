def backtest_strategy(df, signals, sl_pct, tp_pct):
    trades = []
    equity = [100.0]
    capital = 100.0
    for _, s in signals.iterrows():
        entry_price = s['price']
        entry_time = s['datetime']
        idx = df.index.get_loc(entry_time)
        sl = entry_price * (1 - sl_pct / 100) if 'long' in s['signal'] else entry_price * (1 + sl_pct / 100)
        tp = entry_price * (1 + tp_pct / 100) if 'long' in s['signal'] else entry_price * (1 - tp_pct / 100)

        result = 'none'
        for i in range(idx + 1, len(df)):
            price = df['Low'][i] if 'long' in s['signal'] else df['High'][i]
            if ('long' in s['signal'] and price <= sl) or ('short' in s['signal'] and price >= sl):
                capital -= capital * (sl_pct / 100)
                result = 'loss'
                break
            price = df['High'][i] if 'long' in s['signal'] else df['Low'][i]
            if ('long' in s['signal'] and price >= tp) or ('short' in s['signal'] and price <= tp):
                capital += capital * (tp_pct / 100)
                result = 'win'
                break
        equity.append(capital)
        trades.append({"datetime": entry_time, "signal": s['signal'], "entry": entry_price, "result": result})
    return pd.DataFrame(trades), equity
