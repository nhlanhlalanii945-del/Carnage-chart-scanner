import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# ==========================================
# ❄️ GLOBAL TERMINAL THEME INJECTION
# ==========================================
st.set_page_config(page_title="Carnage Trading Terminal v5.2", page_icon="❄️", layout="wide")

st.markdown("""
    <style>
    /* Main Background - Frozen Night Void */
    .stApp {
        background: linear-gradient(135deg, #050b11 0%, #091320 50%, #050a0f 100%);
        color: #e2e8f0;
    }
    
    /* Glacial Headers */
    h1, h2, h3 {
        color: #a5f3fc !important;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 15px rgba(165, 243, 252, 0.4);
        font-weight: 800;
    }
    
    /* Frosted Glass Cards Container */
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(10, 23, 39, 0.75);
        border: 1px solid rgba(165, 243, 252, 0.15);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }
    
    /* Navigation Tab Styling Customization */
    button[data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-size: 16px !important;
        font-family: monospace !important;
        font-weight: bold !important;
        background-color: transparent !important;
        transition: all 0.3s ease;
    }
    button[aria-selected="true"] {
        color: #38bdf8 !important;
        border-bottom-color: #38bdf8 !important;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
    }
    
    /* Ice Blue Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #0f172a 0%, #0284c7 100%) !important;
        color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 6px !important;
        box-shadow: 0 0 15px rgba(2, 132, 199, 0.4);
        transition: all 0.3s ease;
        font-weight: bold;
        font-size: 18px !important;
        padding: 12px 0px !important;
        width: 100%;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%) !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.7);
        transform: scale(1.01);
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<h1 style='text-align: center;'>❄️ CARNAGE TRADING TERMINAL V5.2 ❄️</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #e11d48; font-family: monospace; font-weight: bold;'>⚠️ NOTE: API data feeds hold a structural 15-minute delay. Use targets as pips/dist markers on MT5.</p>", unsafe_allow_html=True)
st.write("---")

# ==========================================
# 🎛️ SHARED CONTROL CENTER (GLOBAL INPUTS)
# ==========================================
col_ui1, col_ui2, col_ui3 = st.columns(3)

with col_ui1:
    asset_options = ["GOLD (XAUUSD)", "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD"]
    selected_asset = st.selectbox("💱 TARGET ASSET BLOCK:", asset_options)

with col_ui2:
    timeframe_options = [
        "M5 (5 Minute Scalp)", 
        "M15 (15 Minute Scalp)", 
        "H1 (1 Hour Intraday)", 
        "H4 (4 Hour Swing)", 
        "D1 (Daily Swing)",
        "Weekly (Macro Trend)"
    ]
    selected_tf = st.selectbox("⏳ RUNTIME TIMEFRAME:", timeframe_options)

with col_ui3:
    account_balance = st.number_input("💰 ACCOUNT CAPITALIZATION ($):", value=1000.0, step=100.0)

# Master Ticker Mappings
ticker_map = {
    "GOLD (XAUUSD)": "GC=F",
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "USDJPY": "JPY=X",
    "AUDUSD": "AUDUSD=X",
    "USDCAD": "CAD=X"
}
target_ticker = ticker_map[selected_asset]

# Dynamic Data Configurations
if "M5" in selected_tf:
    tf_interval, tf_period, lookback_bars = "5m", "5d", 100  
elif "M15" in selected_tf:
    tf_interval, tf_period, lookback_bars = "15m", "1mo", 100
elif "H1" in selected_tf:
    tf_interval, tf_period, lookback_bars = "1h", "1mo", 48   
elif "H4" in selected_tf:
    tf_interval, tf_period, lookback_bars = "1h", "3mo", 50   
elif "D1" in selected_tf:
    tf_interval, tf_period, lookback_bars = "1d", "1y", 30   
elif "Weekly" in selected_tf:
    tf_interval, tf_period, lookback_bars = "1wk", "2y", 52

st.write("---")

# Helper Data Extraction Engine
def fetch_processed_data():
    df = yf.Ticker(target_ticker).history(period=tf_period, interval=tf_interval)
    if not df.empty and "H4" in selected_tf:
        # Custom 4-Hour Resampling Algorithm
        df = df.resample('4H').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        }).dropna()
    return df

# ==========================================
# 🧭 SYSTEM NAVIGATION MATRIX (TABS)
# ==========================================
tab_v4, tab_v5 = st.tabs(["🧬 RETAIL PULLBACK MATRIX (V4)", "🏛️ INSTITUTIONAL SMC SNIPER (V5)"])

# ==========================================
# STRATEGY TAB 1: FIBONACCI + STOCHASTIC (V4)
# ==========================================
with tab_v4:
    st.markdown("### 🧬 Strategy Overview")
    st.write("Tracks momentum pullbacks into critical Fibonacci retracement fields verified via Stochastic exhaustion filters.")
    
    if st.button("🧊 RUN RETAIL MATRIX SCAN"):
        with st.spinner("❄️ Gathering data feeds and running Fibonacci projection layouts..."):
            df = fetch_processed_data()
            
            if df.empty or len(df) < lookback_bars:
                st.error("⚠️ Data structural sync limitation. Re-execute the engine scan block.")
            else:
                df['Close'] = df['Close'].astype(float)
                df['High'] = df['High'].astype(float)
                df['Low'] = df['Low'].astype(float)
                
                current_price = float(df['Close'].iloc[-1])
                recent_data = df.tail(lookback_bars)
                
                df['Stoch_Low'] = df['Low'].rolling(window=14).min()
                df['Stoch_High'] = df['High'].rolling(window=14).max()
                stoch_denom = df['Stoch_High'] - df['Stoch_Low']
                df['%K'] = np.where(stoch_denom > 0, 100 * ((df['Close'] - df['Stoch_Low']) / stoch_denom), 50)
                df['%D'] = df['%K'].rolling(window=3).mean()
                current_k = float(df['%K'].iloc[-1])
                current_d = float(df['%D'].iloc[-1])
                
                fib_high = float(recent_data['High'].max())
                fib_low = float(recent_data['Low'].min())
                fib_range = (fib_high - fib_low) if (fib_high - fib_low) > 0 else 0.0001
                
                short_ema = df['Close'].rolling(window=10).mean().iloc[-1]
                long_ema = df['Close'].rolling(window=30).mean().iloc[-1]
                market_trend = "BULLISH" if short_ema >= long_ema else "BEARISH"
                
                fib_500 = fib_high - (0.500 * fib_range) if market_trend == "BULLISH" else fib_low + (0.500 * fib_range)
                fib_618 = fib_high - (0.618 * fib_range) if market_trend == "BULLISH" else fib_low + (0.618 * fib_range)
                
                signal, confidence = "STANDBY", 50
                sl_buffer = 4.0 if "GOLD" in selected_asset else (0.0025 if "JPY" not in selected_asset else 0.30)
                
                if market_trend == "BULLISH":
                    if current_price <= fib_500 and (current_k < 35 or current_d < 35):
                        signal, confidence = "BUY", 88
                        reason = f"Price tracing optimal discount zones below 50% Fib ({fib_500:.4f}). Stochastic oversold line acts as final validation."
                        stop_loss = fib_low - (sl_buffer * 0.5)
                        take_profit = fib_high
                    else:
                        signal, confidence = "BUY", 65
                        reason = "Upward trend active. Spot pricing structural execution parameters resting at baseline ranges."
                        stop_loss = current_price - sl_buffer
                        take_profit = fib_high
                else:
                    if current_price >= fib_500 and (current_k > 65 or current_d > 65):
                        signal, confidence = "SELL", 87
                        reason = f"Price matching heavy premium extensions above 50% Fib ({fib_500:.4f}). Short sellers loading blocks under overbought parameters."
                        stop_loss = fib_high + (sl_buffer * 0.5)
                        take_profit = fib_low
                    else:
                        signal, confidence = "SELL", 62
                        reason = "Bearish configuration holds. Spot trading below active structural resistance zones."
                        stop_loss = current_price + sl_buffer
                        take_profit = fib_low
                
                applied_risk_pct = 2.0 if confidence >= 80 else 0.5
                cash_at_risk = account_balance * (applied_risk_pct / 100.0)
                sl_dist = abs(current_price - stop_loss) if abs(current_price - stop_loss) > 0 else 0.0001
                
                if "GOLD" in selected_asset: calculated_lots = cash_at_risk / (sl_dist * 100.0)
                elif "JPY" in selected_asset: calculated_lots = cash_at_risk / ((sl_dist / 0.01) * 10.0)
                else: calculated_lots = cash_at_risk / ((sl_dist / 0.0001) * 10.0)
                final_lot_size = max(0.01, round(calculated_lots, 2))
                
                c1, c2, c3 = st.columns(3)
                c1.metric("🧊 Spot Price", f"${current_price:.2f}" if "GOLD" in selected_asset else f"{current_price:.5f}")
                c1.metric("📊 Stochastic %K", f"{current_k:.2f}")
                c2.metric("🟡 Fib 50.0% Line", f"${fib_500:.2f}" if "GOLD" in selected_asset else f"{fib_500:.5f}")
                c2.metric("📈 Vector Trend", market_trend)
                c3.metric("🔵 Fib 61.8% Line", f"${fib_618:.2f}" if "GOLD" in selected_asset else f"{fib_618:.5f}")
                
                st.write("---")
                st.markdown(f"## ⚡ V4 SIGNAL OUTPUT: **{signal}** (Confidence: {confidence}%)")
                st.info(f"📋 **System Logic Breakdown:** {reason}")
                
                st.markdown("### 🎯 TARGET EXECUTION PROTECTION MATRIX")
                o1, o2, o3, o4 = st.columns(4)
                o1.metric("⚡ ENTRY PRICE", f"${current_price:.2f}" if "GOLD" in selected_asset else f"{current_price:.5f}")
                o2.metric("🛑 STOP LOSS (SL)", f"${stop_loss:.2f}" if "GOLD" in selected_asset else f"{stop_loss:.5f}")
                o3.metric("🟢 TAKE PROFIT (TP)", f"${take_profit:.2f}" if "GOLD" in selected_asset else f"{take_profit:.5f}")
                o4.metric("⚖️ LOT SIZING", f"{final_lot_size} Lots")

# ==========================================
# STRATEGY TAB 2: SMART MONEY CONCEPTS (V5)
# ==========================================
with tab_v5:
    st.markdown("### 🏛️ Strategy Overview")
    st.write("Scans historical high/low ranges for fake-outs (**Liquidity Sweeps**) and tracks institutional reversals via **Market Structure Shifts (MSS)**.")
    
    if st.button("🧊 RUN INSTI-SMC SNIPER SCAN"):
        with st.spinner("❄️ Isolating range boundaries and checking institutional liquidity pools..."):
            df = fetch_processed_data()
            
            if df.empty or len(df) < lookback_bars:
                st.error("⚠️ Data connection sync issue. Hit target trigger again.")
            else:
                df['Close'] = df['Close'].astype(float)
                df['High'] = df['High'].astype(float)
                df['Low'] = df['Low'].astype(float)
                
                current_price = float(df['Close'].iloc[-1])
                
                local_structure = df.tail(25)
                prior_high = float(local_structure['High'].iloc[:-3].max())
                prior_low = float(local_structure['Low'].iloc[:-3].min())
                
                liquidity_sweep_detected = "NONE"
                market_structure_shift = "NO"
                
                recent_lows = df['Low'].iloc[-3:]
                recent_highs = df['High'].iloc[-3:]
                
                if (recent_lows.min() < prior_low) and (current_price > prior_low):
                    liquidity_sweep_detected = "BULLISH SWEEP"
                elif (recent_highs.max() > prior_high) and (current_price < prior_high):
                    liquidity_sweep_detected = "BEARISH SWEEP"
                    
                short_ema = df['Close'].rolling(window=7).mean().iloc[-1]
                long_ema = df['Close'].rolling(window=21).mean().iloc[-1]
                macro_trend = "BULLISH" if short_ema >= long_ema else "BEARISH"
                
                if (short_ema > long_ema) and (df['Close'].iloc[-3] <= df['Close'].rolling(window=21).mean().iloc[-3]):
                    market_structure_shift = "BULLISH CHoCH"
                elif (short_ema < long_ema) and (df['Close'].iloc[-3] >= df['Close'].rolling(window=21).mean().iloc[-3]):
                    market_structure_shift = "BEARISH CHoCH"
                    
                signal, confidence = "STANDBY", 50
                sl_buffer = 4.5 if "GOLD" in selected_asset else (0.0022 if "JPY" not in selected_asset else 0.28)
                
                if macro_trend == "BULLISH":
                    if "BULLISH" in liquidity_sweep_detected or "BULLISH" in market_structure_shift:
                        signal, confidence = "BUY", 94
                        reason = f"Smart money swept retail stop losses below {prior_low:.2f}. Immediate institutional displacement confirms structural market shift."
                        stop_loss = float(recent_lows.min()) - (sl_buffer * 0.2)
                        take_profit = float(df['High'].tail(100).max())
                    else:
                        signal, confidence = "BUY", 70
                        reason = "Bullish structure holds. Trading standard baseline expansion ranges."
                        stop_loss = current_price - sl_buffer
                        take_profit = current_price + (sl_buffer * 2)
                else:
                    if "BEARISH" in liquidity_sweep_detected or "BEARISH" in market_structure_shift:
                        signal, confidence = "SELL", 93
                        reason = f"Buy-side liquidity swept above structural highs at {prior_high:.2f}. Big banks trapped breakout buyers before a fast drop."
                        stop_loss = float(recent_highs.max()) + (sl_buffer * 0.2)
                        take_profit = float(df['Low'].tail(100).min())
                    else:
                        signal, confidence = "SELL", 65
                        reason = "Order flow remains bearish. Waiting for formal liquidity grab validation."
                        stop_loss = current_price + sl_buffer
                        take_profit = current_price - (sl_buffer * 2)
                
                applied_risk_pct = 3.0 if confidence >= 88 else 1.0
                cash_at_risk = account_balance * (applied_risk_pct / 100.0)
                sl_dist = abs(current_price - stop_loss) if abs(current_price - stop_loss) > 0 else 0.0001
                
                if "GOLD" in selected_asset: calculated_lots = cash_at_risk / (sl_dist * 100.0)
                elif "JPY" in selected_asset: calculated_lots = cash_at_risk / ((sl_dist / 0.01) * 10.0)
                else: calculated_lots = cash_at_risk / ((sl_dist / 0.0001) * 10.0)
                final_lot_size = max(0.01, round(calculated_lots, 2))
                
                cc1, cc2, cc3 = st.columns(3)
                cc1.metric("🧊 Live Price", f"${current_price:.2f}" if "GOLD" in selected_asset else f"{current_price:.5f}")
                cc1.metric("🕵️‍♂️ Liquidity Mapping", liquidity_sweep_detected)
                cc2.metric("🛑 Upper Pool Ceiling", f"${prior_high:.2f}" if "GOLD" in selected_asset else f"{prior_high:.5f}")
                cc2.metric("⚡ Structural Shift", market_structure_shift if market_structure_shift != "NO" else "STABLE")
                cc3.metric("🟢 Lower Pool Floor", f"${prior_low:.2f}" if "GOLD" in selected_asset else f"{prior_low:.5f}")
                
                st.write("---")
                st.markdown(f"## ⚡ V5 SMC SIGNAL OUTPUT: **{signal}** (Confidence: {confidence}%)")
                st.info(f"🏛️ **SMC Analysis Breakdown:** {reason}")
                
                st.markdown("### 🎯 TARGET EXECUTION PROTECTION MATRIX")
                oo1, oo2, oo3, oo4 = st.columns(4)
                oo1.metric("⚡ ENTRY PRICE", f"${current_price:.2f}" if "GOLD" in selected_asset else f"{current_price:.5f}")
                oo2.metric("🛑 STOP LOSS (SL)", f"${stop_loss:.2f}" if "GOLD" in selected_asset else f"{stop_loss:.5f}")
                oo3.metric("🟢 TAKE PROFIT (TP)", f"${take_profit:.2f}" if "GOLD" in selected_asset else f"{take_profit:.5f}")
                oo4.metric("⚖️ LOT SIZING", f"{final_lot_size} Lots")
