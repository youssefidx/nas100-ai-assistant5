import pandas as pd

def generate_trade_signals(df, zones, use_volume=True, session_start=None):
    signals = []
    for z in zones:
        idx = df.index.get_loc(z['datetime'])
        if idx >= len(df) - 1:
            continue
        row = df.iloc[idx]
        next_row = df.iloc[idx + 1]
        if session_start and row.name.time() < session_start:
            continue

        signal = None
        if next_row['Close'] > z['resistance']:
            if not use_volume or next_row['Volume'] > df['Volume'].rolling(20).mean().iloc[idx]:
                signal = 'breakout_long'
        elif next_row['Close'] < z['support']:
            if not use_volume or next_row['Volume'] > df['Volume'].rolling(20).mean().iloc[idx]:
                signal = 'breakout_short'

        if signal:
            signals.append({"datetime": next_row.name, "price": next_row['Close'], "signal": signal})
    return pd.DataFrame(signals)
