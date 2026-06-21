import streamlit as st
import yfinance as yf
import pandas as pd

# Page Configuration for Mobile Layout
st.set_page_config(page_title="Carnage Scanner", page_icon="🧲", layout="centered")

st.markdown("<h2 style='text-align: center; color: #FF4B4B;'>🧲 CARNAGE PA & CRT SCANNER</h2>", unsafe_allow_html=True)
st.write("---")

# User Interface Elements
pairs = ["XAUUSD=X", "EURUSD=X", "GBPUSD=X"]
selected_pair = st.selectbox("🎯 SELECT TARGET ASSET", pairs, index=0)

col1, col2 = st.columns(2)
with col1:
    start_scan = st.button("▶️ START SCAN", use_container_width=True)
with col2:
    clear_logs = st.button("❌ CLEAR", use_container_width=True)

# Main Scanner Execution
if start_scan:
    st.info(f"🔄 Fetching raw data stream for {selected_pair}...")
    
    try:
        # 1. Fetch High Timeframe (H4) Data for Candle Range Theory (CRT)
        h4_data = yf.download(tickers=selected_pair, period="5d", interval="4h")
        
        # Pull exact High and Low parameters of the previous completed H4 candle
        crt_high = float(h4_data['High'].iloc[-2])
        crt_low = float(h4_data['Low'].iloc[-2])
        current_h4_close = float(h4_data['Close'].iloc[-1])
        
        # Simple Price Action Bias rule
        market_bias = "BULLISH" if current_h4_close > crt_high else "BEARISH"
        
        # 2. Fetch Low Timeframe (M5) Data for FVG detection
        m5_data = yf.download(tickers=selected_pair, period="1d", interval="5m")
        
        c1_low = float(m5_data['Low'].iloc[-1])
        c3_high = float(m5_data['High'].iloc[-3])
        c1_high = float(m5_data['High'].iloc[-1])
        c3_low = float(m5_data['Low'].iloc[-3])
        current_price = float(m5_data['Close'].iloc[-1])
        
        # Strict Rule Checking
        bullish_fvg = c1_low > c3_high
        bearish_fvg = c1_high < c3_low
        in_crt_zone = crt_low <= current_price <= crt_high
        
        # Dashboard Readout Display
        st.write("### 📊 Market Data Metrics")
        metrics_df = pd.DataFrame({
            "Metric": ["H4 CRT High", "H4 CRT Low", "Current Market Price", "H4 Structure Bias"],
            "Value": [f"{crt_high:.2f}", f"{crt_low:.2f}", f"{current_price:.2f}", market_bias]
        })
        st.table(metrics_df)
        
        st.write("---")
        st.write("### 🚨 Strategy Confirmation Results")
        
        # 3. Final Alignment Verification
        if market_bias == "BULLISH" and bullish_fvg and in_crt_zone:
            st.success(f"🔥 HIGH CONFIDENCE ALIGNMENT: Bullish Setup Confirmed!\n\nGap Entry Zone: {crt_low:.2f} - {c1_low:.2f}")
        elif market_bias == "BEARISH" and bearish_fvg and in_crt_zone:
            st.success(f"🔥 HIGH CONFIDENCE ALIGNMENT: Bearish Setup Confirmed!\n\nGap Entry Zone: {c1_high:.2f} - {crt_high:.2f}")
        else:
            st.warning("⚠️ Scanner Standby: Raw data values do not match strict strategy parameters. No setup triggered.")
            
    except Exception as e:
        st.error(f"Error accessing feed: {e}")

if clear_logs:
    st.rerun()
