
import matplotlib.pyplot as plt

def plot_trades(df, trades):
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df.index, df['Close'], label='Price')
    for _, trade in trades.iterrows():
        color = 'green' if trade['Result'] == 'Win' else 'red'
        ax.axvline(trade['Time'], color=color, linestyle='--', alpha=0.6)
    ax.set_title("Trade Entries")
    ax.legend()
    return fig

def plot_equity_curve(equity):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(equity, label="Equity Curve", color='blue')
    ax.set_title("Equity Curve")
    ax.set_ylabel("Equity")
    ax.set_xlabel("Trades")
    ax.legend()
    return fig
