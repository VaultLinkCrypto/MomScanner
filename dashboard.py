import streamlit as st
import pandas as pd
import time
from scanner_logic import run_funnel
from engine import MomentumEngine

st.set_page_config(page_title="VaultLink Scanner", layout="wide")
st.title("🚀 MomScanner: Persistent Trend Monitor")

# --- 1. PERSISTENT MEMORY ---
if 'engine' not in st.session_state:
    st.session_state.engine = MomentumEngine(alpha=0.1) # Alpha 0.1 for even smoother SOFI moves

# --- 2. SIDEBAR ---
with st.sidebar:
    st.header("Settings")
    ticker_input = st.text_area("Watchlist (Comma Separated)", "TSLA,NVDA,AAPL,AMD,SOFI,SPY")
    watchlist = [s.strip().upper() for s in ticker_input.split(",") if s.strip()]
    
    st.divider()
    # The Toggle Switch that replaces the button
    run_live = st.toggle("🛰️ Start Live Monitoring", value=False)
    
    if st.button("Clear Engine Memory"):
        st.session_state.engine.active_tickers.clear()
        st.session_state.engine.scores.clear()
        st.rerun()

# --- 3. LIVE DISPLAY ---
table_placeholder = st.empty()

if run_live:
    # Anchor the rows so they never move
    master_df = pd.DataFrame({'Ticker': watchlist})

    while True:
        # Fetch data for the FULL watchlist
        new_data_df = run_funnel(watchlist, st.session_state.engine)
        
        # Merge onto Master to keep rows STATIC
        display_df = pd.merge(master_df, new_data_df, on='Ticker', how='left')

        with table_placeholder.container():
            st.subheader(f"Monitoring {len(display_df)} Tickers (Static View)")
            
            # Use styling to highlight Active trades
            st.dataframe(
                display_df.style.map(
                    lambda x: 'background-color: #1b5e20; color: white; font-weight: bold' if x == '🔥 ACTIVE' else '',
                    subset=['Status']
                ),
                use_container_width=True,
                hide_index=True
            )
            st.caption(f"Last Update: {time.strftime('%H:%M:%S')} | Rows are anchored. No vanishing tickers.")
        
        time.sleep(1) # Refresh rate
else:
    st.info("Toggle 'Start Live Monitoring' to lock your watchlist into the stable display.")
