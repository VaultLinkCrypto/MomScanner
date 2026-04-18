import streamlit as st
import pandas as pd
import time
from scanner_logic import run_funnel
from engine import MomentumEngine

# 1. Page Configuration
st.set_page_config(page_title="VaultLink Scanner", layout="wide")
st.title("🚀 MomScanner: Live Lotto Sniper")

# 2. Initialize the Engine in 'Memory' (Session State)
# This prevents the score from resetting every second.
if 'engine' not in st.session_state:
    st.session_state.engine = MomentumEngine(alpha=0.2)

# 3. Sidebar Controls
with st.sidebar:
    st.header("Scanner Controls")
    default_tickers = "TSLA,NVDA,AAPL,AMD,MSFT,META,AMZN,GOOGL,SPY,QQQ"
    ticker_input = st.text_area("Watchlist", default_tickers)
    watchlist = [s.strip().upper() for s in ticker_input.split(",")]
    
    st.divider()
    max_spread = st.slider("Max Option Spread ($)", 0.01, 0.10, 0.05)
    # We use this for 'Highlighting' rather than 'Deleting'
    alert_threshold = st.number_input("Alert Threshold", 0, 100, 70)
    
    run_live = st.toggle("🛰️ Start Live Monitoring", value=False)

# 4. The Live Monitoring Loop
# This placeholder allows us to update the table without refreshing the whole page
placeholder = st.empty()

if run_live:
    while True:
        try:
            # Fetch data using the existing funnel
            df = run_funnel(watchlist)
            
            # Sort by Score so the 'hot' ones are always at the top
            df = df.sort_values(by='Score', ascending=False)
            
            # Add a 'Status' column for visual feedback
            df['Signal'] = df['Score'].apply(lambda x: '🔥 BUY' if x >= alert_threshold else '⏳ WAIT')

            with placeholder.container():
                st.subheader(f"Monitoring {len(df)} Tickers")
                
                # We use a color-coded or styled dataframe
                # This keeps the tickers visible even if they drop to a 40 score
                st.dataframe(
                    df.style.map(
                        lambda x: 'background-color: #2e7d32' if x == '🔥 BUY' else '', 
                        subset=['Signal']
                    ),
                    use_container_width=True,
                    hide_index=True
                )
                
                st.caption(f"Last Update: {time.strftime('%H:%M:%S')} | Alpha: 0.2")

            # Frequency: Update every 1 second
            time.sleep(1)
            
        except Exception as e:
            st.error(f"Loop Error: {e}")
            break
else:
    st.info("Toggle 'Start Live Monitoring' in the sidebar to begin.")
