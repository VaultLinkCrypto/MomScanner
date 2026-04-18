import streamlit as st
import pandas as pd
import time
from scanner_logic import run_funnel

st.set_page_config(page_title="VaultLink Scanner", layout="wide")
st.title("🚀 MomScanner: Persistent Trend Monitor")

with st.sidebar:
    st.header("Settings")
    # Tickers to hunt for (SOFI, TSLA, etc)
    ticker_input = st.text_area("Watchlist", "SOFI,TSLA,NVDA,AAPL,AMD,SPY")
    watchlist = [s.strip().upper() for s in ticker_input.split(",")]
    
    run_live = st.toggle("🛰️ Start Monitoring", value=False)

# This container stays static on the page
table_placeholder = st.empty()

if run_live:
    while True:
        # Fetch only the "Active" tickers from the engine's memory
        df = run_funnel(watchlist)
        
        with table_placeholder.container():
            if not df.empty:
                st.subheader(f"Actively Tracking {len(df)} High-Momentum Moves")
                
                # Sort by Score but keep the same tickers on screen
                st.dataframe(
                    df.sort_values(by='Score', ascending=False),
                    use_container_width=True,
                    hide_index=True
                )
                st.caption(f"Last Update: {time.strftime('%H:%M:%S')} | Hysteresis: 80 Entry / 40 Exit")
            else:
                st.info("Searching the 'Lake' for abnormal momentum (Score > 80)...")
        
        time.sleep(1) # Frequency
