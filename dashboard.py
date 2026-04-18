import streamlit as st
import pandas as pd
import time
from scanner_logic import run_funnel
from engine import MomentumEngine

st.set_page_config(page_title="VaultLink Scanner", layout="wide")
st.title("🚀 MomScanner: Fixed-Row Monitor")

# 1. Initialize Memory
if 'engine' not in st.session_state:
    st.session_state.engine = MomentumEngine()

# 2. Sidebar Controls
with st.sidebar:
    st.header("Settings")
    ticker_input = st.text_area("Watchlist", "TSLA,NVDA,AAPL,AMD,SOFI,SPY,QQQ")
    watchlist = [s.strip().upper() for s in ticker_input.split(",") if s.strip()]
    
    st.divider()
    # The Slider no longer HIDES anything. It only acts as a 'Limit' for your eyes.
    max_spread_limit = st.slider("Max Option Spread Goal ($)", 0.01, 0.20, 0.05)
    
    run_live = st.toggle("🛰️ Start Live Stream", value=False)
    
    if st.button("Reset Scanner Memory"):
        st.session_state.engine.active_tickers.clear()
        st.rerun()

# 3. Main Display Area
placeholder = st.empty()

if run_live:
    # Anchor the Rows: Create a static dataframe based on your list
    anchor_df = pd.DataFrame({'Ticker': watchlist})

    while True:
        # Get new data for ALL 7 tickers
        fresh_data = run_funnel(watchlist, st.session_state.engine)
        
        # Merge onto Anchor: This forces the order to stay the same
        # and prevents any ticker from 'vanishing'
        final_df = pd.merge(anchor_df, fresh_data, on='Ticker', how='left')

        with placeholder.container():
            st.subheader(f"Stable View: Tracking {len(final_df)} Tickers")
            
            # Use Style to highlight, NOT filter.
            def style_rows(row):
                styles = [''] * len(row)
                # Highlight Active Momentum
                if row['Status'] == '🔥 ACTIVE':
                    styles[row.index.get_loc('Status')] = 'background-color: #1b5e20; color: white'
                # Highlight Bad Spreads (Red if above your slider limit)
                if row['Spread'] > max_spread_limit:
                    styles[row.index.get_loc('Spread')] = 'background-color: #b71c1c; color: white'
                return styles

            st.dataframe(
                final_df.style.apply(style_rows, axis=1),
                use_container_width=True,
                hide_index=True
            )
            
            st.caption(f"Update: {time.strftime('%H:%M:%S')} | No tickers will vanish. Rows are static.")

        time.sleep(1)
else:
    st.info("Toggle 'Start Live Stream' to lock the rows and begin monitoring.")
