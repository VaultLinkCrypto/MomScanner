import streamlit as st
import pandas as pd
import time
from scanner_logic import run_funnel

# 1. Page Configuration
st.set_page_config(page_title="VaultLink Scanner", layout="wide")
st.title("🚀 MomScanner: Stable Monitor")

# 2. Sidebar Controls
with st.sidebar:
    st.header("Scanner Controls")
    default_tickers = "TSLA,NVDA,AAPL,AMD,MSFT,META,AMZN,GOOGL,SPY,QQQ"
    ticker_input = st.text_area("Watchlist", default_tickers)
    watchlist = [s.strip().upper() for s in ticker_input.split(",")]
    
    st.divider()
    # We remove the 'Max Spread' and 'Min Score' from the DATA logic
    # and move them to VISUAL logic (highlighting)
    alert_threshold = st.number_input("Alert Threshold (Score)", 0, 100, 70)
    
    run_live = st.toggle("🛰️ Start Live Monitoring", value=False)

# 3. The Stable UI Container
placeholder = st.empty()

if run_live:
    # Initialize a Master Dataframe to keep rows static
    # We fetch the list once to "Anchor" the rows
    master_df = pd.DataFrame({'Ticker': watchlist})
    
    while True:
        try:
            # Fetch the new numbers
            new_data_df = run_funnel(watchlist)
            
            # STABILITY STEP: We 'Merge' the new numbers into our Master List
            # This ensures no ticker vanishes and the order stays exactly as you typed it
            display_df = pd.merge(master_df, new_data_df, on='Ticker', how='left')

            with placeholder.container():
                st.subheader(f"Monitoring {len(display_df)} Tickers")
                
                # USER EXPERIENCE IMPROVEMENT:
                # We use 'style' to highlight winners instead of hiding losers.
                # Sorting is now handled MANUALLY by you clicking the column header.
                st.dataframe(
                    display_df.style.map(
                        lambda x: 'background-color: #1b5e20; color: white' if isinstance(x, float) and x >= alert_threshold else '', 
                        subset=['Score']
                    ),
                    use_container_width=True,
                    hide_index=True
                )
                
                st.caption(f"Last Update: {time.strftime('%H:%M:%S')} | Rows are Static. Click headers to sort manually.")

            time.sleep(1)
            
        except Exception as e:
            st.error(f"Loop Error: {e}")
            break
else:
    st.info("Toggle 'Start Live Monitoring' to lock the rows and begin tracking.")
