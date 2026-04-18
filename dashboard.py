import streamlit as st
import pandas as pd
import time
from scanner_logic import run_funnel
from engine import MomentumEngine

st.set_page_config(page_title="VaultLink Scanner", layout="wide")
st.title("🚀 MomScanner: Persistent Trend Monitor")

# --- CRITICAL: PERSISTENT MEMORY ---
# This ensures the 'VIP Lounge' and 'EMA Scores' never reset.
if 'engine' not in st.session_state:
    st.session_state.engine = MomentumEngine(alpha=0.2)

with st.sidebar:
    st.header("Settings")
    ticker_input = st.text_area("Watchlist", "SOFI,TSLA,NVDA,AAPL,AMD,SPY")
    watchlist = [s.strip().upper() for s in ticker_input.split(",")]
    
    st.divider()
    # Hysteresis Controls
    st.session_state.engine.ENTRY_BAR = st.slider("Entry Threshold (Get In)", 50, 95, 80)
    st.session_state.engine.EXIT_BAR = st.slider("Exit Threshold (Stay In)", 10, 50, 40)
    
    run_live = st.toggle("🛰️ Start Monitoring", value=False)

table_placeholder = st.empty()

if run_live:
    # 1. Anchor the rows. These tickers will NEVER move or disappear.
    master_df = pd.DataFrame({'Ticker': watchlist})

    while True:
        # 2. Pass the persistent engine into the funnel
        new_data_df = run_funnel(watchlist, st.session_state.engine)
        
        # 3. Merge new data onto our Anchor List
        # This keeps the rows in the EXACT order you typed them.
        display_df = pd.merge(master_df, new_data_df, on='Ticker', how='left')

        with table_placeholder.container():
            st.subheader(f"Monitoring {len(display_df)} Tickers (Static Rows)")
            
            # 4. Display Logic
            # We show EVERY ticker in your list. 
            # We use colors to show which ones are 'Active'
            st.dataframe(
                display_df.style.map(
                    lambda x: 'background-color: #1b5e20; color: white;' if x == 'ACTIVE' else '',
                    subset=['Status']
                ),
                use_container_width=True,
                hide_index=True
            )
            st.caption(f"Last Update: {time.strftime('%H:%M:%S')} | Logic: Row Anchoring + Session Memory")
        
        time.sleep(1)
else:
    st.info("Toggle 'Start Monitoring' to lock the spreadsheet rows.")
