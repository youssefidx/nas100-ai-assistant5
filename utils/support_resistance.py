def detect_zones(df, lookback=100):
    zones = []
    for i in range(lookback, len(df)):
        high_zone = df['High'][i - lookback:i].max()
        low_zone = df['Low'][i - lookback:i].min()
        zones.append({"datetime": df.index[i], "support": low_zone, "resistance": high_zone})
    return zones
