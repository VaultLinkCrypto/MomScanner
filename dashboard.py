import streamlit as st
import pandas as pd
from scanner_logic import run_funnel, MOCK_MODE

st.set_page_config(page_title="VaultLink Scanner", layout="wide")
st.title("🚀 MomScanner: Lotto Sniper")

with st.sidebar:
    st.header("Controls")
    # Display Mode Status
    if MOCK_MODE:
        st.warning("⚠️ MODE: WEEKEND SIMULATOR")
    else:
        st.success("✅ MODE: LIVE TRADIER L2")

    default_tickers = "TSLA,NVDA,AAPL,AMD,MSFT,META,AMZN,GOOGL,SPY,QQQ"
    ticker_input = st.text_area("Watchlist", default_tickers)
    watchlist = [s.strip().upper() for s in ticker_input.split(",")]

    st.divider()
    max_spread = st.slider("Max Option Spread ($)", 0.01, 0.10, 0.05)
    min_score = st.number_input("Min Momentum Score", 0, 100, 40)
    
    if st.button("Reset Filters"):
        st.rerun()

if st.button('🔍 Run Momentum Scanner'):
    df = run_funnel(watchlist)
    
    # Filter the results based on your BA requirements
    filtered_df = df[(df['Spread'] <= max_spread) & (df['Score'] >= min_score)]
    
    st.subheader(f"Results ({len(filtered_df)} found)")
    # Sortable Spreadsheet View
    st.dataframe(
        filtered_df.sort_values(by='Score', ascending=False), 
        use_container_width=True, 
        hide_index=True
    )
else:
    st.info("Scanner Ready. Click above to scan the 'Lake'.")
