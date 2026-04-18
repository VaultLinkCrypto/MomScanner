import streamlit as st
import pandas as pd
import time
import random

# --- 1. THE BRAIN (Internalized Engine) ---
class MomentumEngine:
    def __init__(self, alpha=0.3):
        self.alpha = alpha
        self.scores = {}
        self.active_tickers = set()

    def calculate_score(self, ticker):
        # Simulated Level 2 Data (Internalized)
        bid_vol = random.randint(100, 1000)
        ask_vol = random.randint(100, 1000)
        
        raw_ratio = (bid_vol - ask_vol) / (bid_vol + ask_vol)
        raw_score = ((raw_ratio + 1) / 2) * 100
        
        prev_score = self.scores.get(ticker, 50.0)
        smoothed_score = (raw_score * self.alpha) + (prev_score * (1 - self.alpha))
        self.scores[ticker] = smoothed_score
        
        if smoothed_score >= 80: self.active_tickers.add(ticker)
        elif smoothed_score < 40: self.active_tickers.discard(ticker)
        
        return round(smoothed_score, 2)

# --- 2. THE DASHBOARD CONFIG ---
st.set_page_config(page_title="MomScanner FINAL", layout="wide")

if 'engine' not in st.session_state:
    st.session_state.engine = MomentumEngine()

st.title("🚀 MomScanner: Unified Stable Monitor")
st.write(f"Current File Running: `{__file__}`") # PROOF OF PATH

# --- 3. SIDEBAR ---
with st.sidebar:
    st.header("Settings")
    ticker_input = st.text_area("Watchlist", "SOFI,TSLA,NVDA,AAPL,AMD,SPY,QQQ")
    watchlist = [s.strip().upper() for s in ticker_input.split(",") if s.strip()]
    
    st.divider()
    run_live = st.toggle("🛰️ Start Live Monitoring", value=False)
    
    if st.button("Reset All Memory"):
        st.session_state.engine = MomentumEngine()
        st.rerun()

# --- 4. THE LIVE LOOP ---
placeholder = st.empty()

if run_live:
    anchor_df = pd.DataFrame({'Ticker': watchlist})
    
    while True:
        # Generate Fresh Data
        results = []
        for ticker in watchlist:
            score = st.session_state.engine.calculate_score(ticker)
            results.append({
                'Ticker': ticker,
                'Score': score,
                'Status': '🔥 ACTIVE' if ticker in st.session_state.engine.active_tickers else '🔎 SCAN',
                'Volume_M': round(random.uniform(1.0, 99.0), 1),
                'Price': round(random.uniform(10.0, 200.0), 2)
            })
        
        new_data = pd.DataFrame(results)
        # STABILITY MERGE
        final_df = pd.merge(anchor_df, new_data, on='Ticker', how='left')

        with placeholder.container():
            # PULSE INDICATOR
            pulse = "🟢" if int(time.time()) % 2 == 0 else "⚪"
            st.subheader(f"{pulse} LIVE FEED | Rows Anchored")
            
            st.dataframe(
                final_df.sort_values(by='Score', ascending=False),
                width=1200, # Using explicit width for 2026 compatibility
                hide_index=True
            )
            st.caption(f"Last Terminal Tick: {time.strftime('%H:%M:%S')}")
        
        time.sleep(1)
else:
    st.info("Flip the switch to lock rows and start the engine.")
