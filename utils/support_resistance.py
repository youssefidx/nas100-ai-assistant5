
import pandas as pd

def detect_support_resistance(df, bins=20):
    df['Bin'] = pd.cut(df['Low'], bins)
    grouped = df.groupby('Bin')
    zones = []

    for bin_name, group in grouped:
        if len(group) > 10:
            support = group['Low'].min()
            resistance = group['High'].max()
            zones.append({'support': support, 'resistance': resistance})
    return zones
