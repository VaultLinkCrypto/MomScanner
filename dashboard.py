import streamlit as st
import pandas as pd
import time
from scanner_logic import run_funnel
from engine import MomentumEngine

st.set_page_config(page_title="VaultLink Scanner", layout="wide")
st.title("🚀 MomScanner: Stable Live Monitor")

# 1. Initialize Persistent Memory
if 'engine' not in st.session_state:
    st.session_state.engine = MomentumEngine(alpha=0.3)

# 2. Sidebar
with st.sidebar:
    st.header("Settings")
    ticker_input = st.text_area("Watchlist", "TSLA,NVDA,AAPL,AMD,SOFI,SPY,QQQ")
    watchlist = [s.strip().upper() for s in ticker_input.split(",") if s.strip()]
    
    st.divider()
    # THIS IS THE TOGGLE. If you see a button, the code didn't update.
    run_live = st.toggle("🛰️ Start Live Monitoring", value=False)
    
    if st.button("Reset Memory"):
        st.session_state.engine.active_tickers.clear()
        st.rerun()

# 3. Display
placeholder = st.empty()

if run_live:
    # Anchor the rows
    anchor_df = pd.DataFrame({'Ticker': watchlist})

    while True:
        # Get data
        fresh_data = run_funnel(watchlist, st.session_state.engine)
        
        # Merge onto anchor
        final_df = pd.merge(anchor_df, fresh_data, on='Ticker', how='left')

        with placeholder.container():
            st.subheader(f"Status: LIVE | Tracking {len(final_df)} Tickers")
            
            # Show the table
            st.dataframe(
                final_df.sort_values(by='Score', ascending=False),
                use_container_width=True,
                hide_index=True
            )
            st.caption(f"Last Terminal Tick: {time.strftime('%H:%M:%S')}")

        # Force a 1-second wait before the next loop
        time.sleep(1)
else:
    st.info("Flip the 'Start Live Monitoring' switch in the sidebar to begin.")
