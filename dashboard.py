import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="VaultLink Scanner", layout="wide")
st.title("🚀 MomScanner: Lotto Sniper")

# 2. Sidebar Filters (The 'BA' Controls)
with st.sidebar:
    st.header("Controls")
    max_spread = st.slider("Max Option Spread ($)", 0.01, 0.10, 0.04)
    min_score = st.number_input("Min Momentum Score", 0, 100, 70)
    if st.button("Reset All Filters"):
        st.rerun()

# 3. Data Simulation (This will be replaced by your Funnel Logic)
data = {
    'Ticker': ['TSLA', 'NVDA', 'AAPL', 'AMD', 'SPY', 'QQQ'],
    'Score': [88.5, 94.2, 42.1, 76.8, 65.0, 81.2],
    'Option_Price': [0.45, 0.88, 0.05, 0.12, 0.95, 0.75],
    'Spread': [0.01, 0.01, 0.04, 0.02, 0.01, 0.01],
    'Volume_M': [25.1, 44.3, 12.9, 18.2, 110.5, 85.1]
}
df = pd.DataFrame(data)

# 4. Applying the "Laser Focus" Filters
filtered_df = df[(df['Spread'] <= max_spread) & (df['Score'] >= min_score)]

# 5. The Spreadsheet Display
st.subheader(f"Found {len(filtered_df)} Opportunities")
# st.dataframe allows users to click headers to sort automatically
st.dataframe(filtered_df.sort_values(by='Score', ascending=False), 
             use_container_width=True, 
             hide_index=True)

# 6. Status Footer
st.caption("Data Source: Tradier L2 | Logic: Exponential Smoothing (Alpha=0.2)")
