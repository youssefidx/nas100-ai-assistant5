import matplotlib.pyplot as plt

def plot_candles_with_trades(df, trades):
    fig, ax = plt.subplots(figsize=(14, 6))
    df_plot = df[-200:].copy()
    ax.plot(df_plot.index, df_plot['Close'], label='Close Price')
    for _, trade in trades.iterrows():
        color = 'green' if 'long' in trade['signal'] else 'red'
        marker = '^' if 'long' in trade['signal'] else 'v'
        ax.plot(trade['datetime'], trade['entry'], marker=marker, color=color, markersize=10)
    ax.set_title("Trades on Chart")
    ax.legend()
    return fig

def plot_equity_curve(equity):
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(equity, label='Equity Curve', color='blue')
    ax.set_title("Equity Curve")
    ax.set_ylabel("Capital")
    ax.set_xlabel("Trade Number")
    ax.grid()
    return fig
