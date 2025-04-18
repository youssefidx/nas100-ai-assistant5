import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils.support_resistance import detect_support_resistance
from utils.trade_signals import generate_trade_signals
from utils.backtest import backtest_strategy
from utils.plots import plot_trades, plot_equity_curve
from utils.download import get_table_download_link

st.set_page_config(page_title="NAS100 AI Trading Assistant", layout="wide")

st.title("📊 NAS100 AI Trading Assistant")

uploaded_file = st.file_uploader("Upload NAS100 CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'])

    st.write("Sample Data", df.head())

    # Parameters
    sl_pct = st.sidebar.slider("Stop Loss (%)", 1.0, 2.5, 1.5)
    tp_pct = st.sidebar.slider("Take Profit (%)", 3.0, 10.0, 5.0)
    use_volume = st.sidebar.checkbox("Use Volume for Signal Confirmation", value=True)
    session_start = st.sidebar.time_input("Session Start Time", value=pd.to_datetime("09:30").time())

    # Detect Zones
    zones = detect_support_resistance(df)
    st.subheader("Detected Support & Resistance Zones")
    st.write(zones)

    # Generate Signals
    signals = generate_trade_signals(df, zones, use_volume=use_volume, session_start=session_start)
    st.subheader("Generated Signals")
    st.write(signals.head())

    if not signals.empty:
        try:
            # Run Backtest
            trades, equity = backtest_strategy(df, signals, sl_pct, tp_pct)

            st.subheader("Backtest Results")
            st.write("Total Trades:", len(trades))
            st.write("Win Rate:", f"{(trades['Result'] == 'Win').mean() * 100:.2f}%")

            if len(equity) > 1:
                st.write("Total Return:", f"{equity[-1] - equity[0]:.2f}")
            else:
                st.warning("Not enough trades to calculate return.")

            # Download link
            st.markdown(get_table_download_link(trades, filename="trades.csv"), unsafe_allow_html=True)

            # Plotting
            st.subheader("Equity Curve")
            fig1 = plot_equity_curve(equity)
            st.pyplot(fig1)

            st.subheader("Trade Chart")
            fig2 = plot_trades(df, trades)
            st.pyplot(fig2)

        except Exception as e:
            st.error(f"An error occurred during backtesting or plotting: {e}")
    else:
        st.warning("No trade signals generated.")
else:
    st.info("Please upload a CSV file to get started.")
