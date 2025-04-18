
import pandas as pd

def generate_trade_signals(df, zones, use_volume=True, session_start=None):
    signals = []
    if 'datetime' in df.columns:
        df.rename(columns={'datetime': 'Datetime'}, inplace=True)
    df.set_index('Datetime', inplace=True)
    
    for z in zones:
        for i in range(len(df) - 1):
            row = df.iloc[i]
            next_row = df.iloc[i + 1]

            if session_start and row.name.time() < session_start:
                continue

            signal = None
            if next_row['Close'] > z['resistance']:
                if not use_volume or next_row['Volume'] > df['Volume'].rolling(20).mean().iloc[i]:
                    signal = 'breakout_long'
            elif next_row['Close'] < z['support']:
                if not use_volume or next_row['Volume'] > df['Volume'].rolling(20).mean().iloc[i]:
                    signal = 'breakout_short'

            if signal:
                signals.append({
                    'Time': next_row.name,
                    'Entry Price': next_row['Close'],
                    'Direction': signal
                })

    df.reset_index(inplace=True)
    return pd.DataFrame(signals)
