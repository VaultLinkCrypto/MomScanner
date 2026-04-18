import streamlit as st
import pandas as pd
from scanner_logic import run_funnel
import os

# 1. Page Configuration
st.set_page_config(page_title="VaultLink Scanner", layout="wide")
st.title("🚀 MomScanner: Lotto Sniper")

# 2. Sidebar Filters (The 'BA' Controls)
with st.sidebar:
    st.header("Scanner Controls")
    
    # Target Tickers (The 'Lake')
    # Start with a focused list to prevent API rate-limiting
    default_tickers = "TSLA,NVDA,AAPL,AMD,MSFT,META,AMZN,GOOGL,SPY,QQQ"
    ticker_input = st.text_area("Symbols to Scan (Comma Separated)", default_tickers)
    watchlist = [s.strip().upper() for s in ticker_input.split(",")]

    st.divider()

    # Filters
    max_spread = st.slider("Max Option Spread ($)", 0.01, 0.10, 0.04)
    min_score = st.number_input("Min Momentum Score", 0, 100, 70)
    
    if st.button("Reset All Filters"):
        st.cache_data.clear()
        st.rerun()

# 3. Execution Trigger
# We don't want to scan 11,000 tickers every time you move a slider.
# This button triggers the 'Funnel'.
if st.button('🔍 Run Momentum Scanner'):
    with st.spinner('Scanning Market Depth and Option Chains...'):
        try:
            # Call the logic from scanner_logic.py
            # This handles the ETL process
            raw_df = run_funnel(watchlist)
            
            if not raw_df.empty:
                # 4. Applying the "Laser Focus" Filters
                # We filter the results of the scan based on your sidebar inputs
                filtered_df = raw_df[
                    (raw_df['Spread'] <= max_spread) & 
                    (raw_df['Score'] >= min_score)
                ]

                # 5. The Spreadsheet Display
                st.subheader(f"Found {len(filtered_df)} Opportunities")
                
                # Sort by Score descending by default for priority
                display_df = filtered_df.sort_values(by='Score', ascending=False)
                
                # Render the sortable dataframe
                st.dataframe(
                    display_df, 
                    use_container_width=True, 
                    hide_index=True
                )
            else:
                st.warning("Scanner returned no results. Check if the market is open or your API token is valid.")
        
        except Exception as e:
            st.error(f"Critical Engine Failure: {e}")
            st.info("Ensure your TRADIER_TOKEN is set in GitHub Secrets.")

else:
    st.info("Click the 'Run Momentum Scanner' button to start the data funnel.")

# 6. Status Footer
st.divider()
col1, col2 = st.columns(2)
with col1:
    st.caption("Data Source: Tradier Level 2 (Pending Upgrade)")
with col2:
    st.caption("Execution Engine: VaultLinkCrypto / MomScanner v1.0")
