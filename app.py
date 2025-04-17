import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import time
from utils.support_resistance import detect_zones
from utils.trade_signals import generate_trade_signals
from utils.backtest import backtest_strategy
from utils.plots import plot_candles_with_trades, plot_equity_curve
from utils.download import download_trade_log

st.set_page_config(page_title="NAS100 AI Trading Assistant", layout="wide", page_icon="📈")
st.title("📈 NAS100 AI Trading Assistant")

st.sidebar.header("Upload NAS100 Price Data")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=['Datetime'])
    df.set_index('Datetime', inplace=True)
    st.success("Data uploaded successfully!")

    tf = st.sidebar.selectbox("Timeframe", ["5min", "15min"])
    sl_pct = st.sidebar.slider("Stop Loss %", 1.0, 2.5, 1.5)
    tp_pct = st.sidebar.slider("Take Profit %", 3.0, 10.0, 5.0)
    use_volume = st.sidebar.checkbox("Use Volume Confirmation", value=True)
    session_start = time(9, 30)

    st.subheader("Detected Support & Resistance Zones")
    zones = detect_zones(df)
    st.write(zones)

    st.subheader("Trade Signals")
    signals = generate_trade_signals(df, zones, use_volume=use_volume, session_start=session_start)
    st.write(signals.head())

    st.subheader("Backtest Performance")
    trades, equity = backtest_strategy(df, signals, sl_pct, tp_pct)
    st.write("Win Rate:", f"{(trades['result'] == 'win').mean() * 100:.2f}%")
    st.write("Total Return:", f"{equity[-1] - equity[0]:.2f}%")

    st.subheader("Candlestick Chart with Trades")
    fig1 = plot_candles_with_trades(df, trades)
    st.pyplot(fig1)

    st.subheader("Equity Curve")
    fig2 = plot_equity_curve(equity)
    st.pyplot(fig2)

    st.subheader("Download Trade Log")
    csv = download_trade_log(trades)
    st.download_button("Download CSV", csv, file_name="nas100_trades.csv", mime="text/csv")

else:
    st.info("Please upload a NAS100 price CSV file to get started.")
