import streamlit as st
import yfinance as yf
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Carnage Scanner", page_icon="🧲", layout="centered")

st.markdown("<h2 style='text-align: center; color: #FF4B4B;'>🧲 CARNAGE AUTOMATED SIGNAL MATRIX</h2>", unsafe_allow_html=True)
st.write("---")

# Risk Management Input Hub
st.write("### 💰 STEP 1: RISK CALCULATOR SETTINGS")
col_bal, col_risk = st.columns(2)
with col_bal:
    account_balance = st.number_input("Account Balance ($)", value=1000.0, step=100.0, format="%.2f")
with col_risk:
    risk_percent = st.number_input("Risk Per Trade (%)", value=1.0, step=0.5, format="%.1f")

# Image Upload Drop-zone
st.write("---")
st.write("### 📸 STEP 2: DROP ACTIVE CHART")
uploaded_file = st.file_uploader("Upload your current MT5 or TradingView screenshot...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="🎯 Analysis Reference Chart", use_container_width=True)
    
    st.write("---")
    st.write("### ⚡ STEP 3: SELECT PAIR & RUN ANALYSIS")
    pairs = ["XAUUSD=X", "EURUSD=X", "GBPUSD=X"]
    selected_pair = st.selectbox("🎯 TARGET ASSET CLASS", pairs, index=0)
    
    if st.button("▶️ EXECUTE AUTO-SCAN & GENERATE SIGNAL", use_container_width=True):
        st.info("🔄 Querying market feeds and running confluence math...")
        
        try:
            # Fetch High Timeframe (H4) Data
            h4_data = yf.download(tickers=selected_pair, period="5d", interval="4h")
            # Flatten columns to completely prevent the 'Series' object error
            if isinstance(h4_data.columns, pd.MultiIndex):
                h4_data.columns = [col[0] for col in h4_data.columns]
                
            crt_high = float(h4_data['High'].iloc[-2])
            crt_low = float(h4_data['Low'].iloc[-2])
            
            # Fetch Low Timeframe (M5) Data
            m5_data = yf.download(tickers=selected_pair, period="1d", interval="5m")
            if isinstance(m5_data.columns, pd.MultiIndex):
                m5_data.columns = [col[0] for col in m5_data.columns]
                
            current_price = float(m5_data['Close'].iloc[-1])
            c1_low = float(m5_data['Low'].iloc[-1])
            c3_high = float(m5_data['High'].iloc[-3])
            c1_high = float(m5_data['High'].iloc[-1])
            c3_low = float(m5_data['Low'].iloc[-3])
            
            # Confluence Rule Calculations
            market_bias = "BULLISH" if current_price > ((crt_high + crt_low) / 2) else "BEARISH"
            bullish_fvg = c1_low > c3_high
            bearish_fvg = c1_high < c3_low
            in_crt_zone = crt_low <= current_price <= crt_high
            
            # Display Extracted Levels
            st.write("#### 📊 Extracted Market Parameters")
            metrics_df = pd.DataFrame({
                "Parameter": ["Current Live Price", "H4 CRT Range High", "H4 CRT Range Low", "Structural Bias Direction"],
                "Value": [f"{current_price:.5f}", f"{crt_high:.5f}", f"{crt_low:.5f}", market_bias]
            })
            st.table(metrics_df)
            
            st.write("---")
            st.write("### 🚨 REAL-TIME TRADE SIGNAL OBJECTIVE")
            
            risk_amount_usd = account_balance * (risk_percent / 100.0)
            
            # 🚨 BULLISH SIGNAL RULES
            if market_bias == "BULLISH" and bullish_fvg and in_crt_zone:
                entry_price = current_price
                stop_loss = crt_low - (crt_low * 0.0005) # Safe buffer below CRT Low
                pip_risk = abs(entry_price - stop_loss)
                
                # Take profit targeting structural high (1:2 Minimum Risk-to-Reward minimum)
                take_profit = entry_price + (pip_risk * 2.0)
                
                # Position Sizing Logic
                if "XAUUSD" in selected_pair:
                    # Gold contract sizing math ($1 move = 100 points)
                    lot_size = risk_amount_usd / (pip_risk * 100.0) if pip_risk > 0 else 0.01
                else:
                    # Standard Forex lot sizing math (1 standard lot = $10 per pip)
                    lot_size = risk_amount_usd / (pip_risk * 100000.0) if pip_risk > 0 else 0.01
                
                st.success(f"🟩 **EXECUTION SIGNAL: BUY / LONG**\n\n"
                           f"🎯 **Entry Price:** {entry_price:.5f}\n\n"
                           f"🛑 **Stop Loss (SL):** {stop_loss:.5f}\n\n"
                           f"🏁 **Take Profit (TP):** {take_profit:.5f}\n\n"
                           f"🔥 **Calculated Lot Size:** {max(lot_size, 0.01):.2f} Lots (Risking ${risk_amount_usd:.2f})")
                           
            # 🚨 BEARISH SIGNAL RULES
            elif market_bias == "BEARISH" and bearish_fvg and in_crt_zone:
                entry_price = current_price
                stop_loss = crt_high + (crt_high * 0.0005) # Safe buffer above CRT High
                pip_risk = abs(stop_loss - entry_price)
                
                take_profit = entry_price - (pip_risk * 2.0)
                
                # Position Sizing Logic
                if "XAUUSD" in selected_pair:
                    lot_size = risk_amount_usd / (pip_risk * 100.0) if pip_risk > 0 else 0.01
                else:
                    lot_size = risk_amount_usd / (pip_risk * 100000.0) if pip_risk > 0 else 0.01
                    
                st.shapes = st.success(f"🟥 **EXECUTION SIGNAL: SELL / SHORT**\n\n"
                           f"🎯 **Entry Price:** {entry_price:.5f}\n\n"
                           f"🛑 **Stop Loss (SL):** {stop_loss:.5f}\n\n"
                           f"🏁 **Take Profit (TP):** {take_profit:.5f}\n\n"
                           f"🔥 **Calculated Lot Size:** {max(lot_size, 0.01):.2f} Lots (Risking ${risk_amount_usd:.2f})")
            else:
                st.warning("⚠️ **MARKET STATUS: STANDBY (NO SETUP)**\n\nLive values do not perfectly match strict algorithmic confluence parameters. Do not force entries here.")
                
        except Exception as e:
            st.error(f"Error executing live matrix scan: {e}")
else:
    st.info("💡 Drop your trading chart screenshot above to initialize the automated Carnage scanning matrix.")
# 1. Fetch the data (Make sure period is at least '5d' so it always has data)
df = yf.download(tickers=selected_pair, period="5d", interval="15m")

# 2. Check if the data came back empty BEFORE running math
if df.empty:
    st.warning("⚠️ Market data stream is temporarily lagging. Tap 'EXECUTE AUTO-SCAN' again to re-fetch.")
else:
    # 3. Put ALL your logic, calculations, and .iloc[-1] code INSIDE this block
    current_price = float(df['Close'].iloc[-1])
    
    # ... (rest of your scanner code, CRT ranges, and signal output goes here)

