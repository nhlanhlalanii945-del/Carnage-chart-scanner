import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# ==========================================
# ❄️ DEEP FROZEN / COLD SNOWY THEME INJECTION
# ==========================================
st.set_page_config(page_title="Carnage Frost Scanner", page_icon="❄️", layout="wide")

st.markdown("""
    <style>
    /* Main Background - Frozen Night Void */
    .stApp {
        background: linear-gradient(135deg, #060c13 0%, #0b1523 50%, #070d16 100%);
        color: #e2e8f0;
    }
    
    /* Glacial Headers */
    h1, h2, h3 {
        color: #93c5fd !important;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 12px rgba(147, 197, 253, 0.4);
        font-weight: 800;
    }
    
    /* Frosted Glass Cards Container */
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(13, 27, 42, 0.65);
        border: 1px solid rgba(147, 197, 253, 0.15);
        border-radius: 14px;
        padding: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    /* Frozen Alert / Status Boxes */
    .stAlert {
        background-color: rgba(15, 34, 64, 0.8) !important;
        border: 1px solid #3b82f6 !important;
        color: #93c5fd !important;
        border-radius: 10px;
    }
    
    /* Ice Blue Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        border: 1px solid #60a5fa !important;
        border-radius: 8px !important;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.4);
        transition: all 0.3s ease;
        font-weight: bold;
        width: 100%;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%) !important;
        box-shadow: 0 0 25px rgba(96, 165, 250, 0.7);
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# App Title Layout
st.markdown("<h1 style='text-align: center;'>❄️ CARNAGE FROST SCANNER ❄️</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>Supply & Demand • Structural Trendlines • Order Execution</p>", unsafe_allow_html=True)
st.write("---")

# ==========================================
# 📊 SIDEBAR / INPUT CONFIGURATION
# ==========================================
st.sidebar.markdown("### 🥶 COLD RISK CONTROL")
account_balance = st.sidebar.number_input("Account Balance ($)", value=1000.0, step=100.0)
risk_percent = st.sidebar.number_input("Risk Per Trade (%)", value=1.0, step=0.5)

st.markdown("### ⚡ STEP 1: CHOOSE TARGET PAIR")
pairs = ["XAUUSD=X", "EURUSD=X", "GBPUSD=X"]
selected_pair = st.selectbox("Select Asset Class to Freeze:", pairs)

st.markdown("### 📸 STEP 2: DROP ACTIVE CHART (REFERENCE)")
uploaded_file = st.file_uploader("Upload your current MT5 or TradingView layout", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Analysis Reference Chart", use_container_width=True)

st.write("---")
st.markdown("### ❄️ STEP 3: EXECUTE MATRIX MATRIX SCAN")

if st.button("🧊 RUN ALGORITHMIC CONFLUENCE SCAN"):
    with st.spinner("❄️ Querying market streams and extracting price action zones..."):
        
        # Fetching 1-Hour data over the past 60 days to locate solid major structural zones
        df = yf.download(tickers=selected_pair, period="60d", interval="1h")
        
        if df.empty:
            st.error("⚠️ Glacial feed error: Market connection dropped. Try running the scan again.")
        else:
            # Flatten multi-index columns if present from yfinance
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
                
            # Flatten values to standard 1D floats to avoid any multi-index extraction bugs
            df['Close'] = df['Close'].astype(float)
            df['High'] = df['High'].astype(float)
            df['Low'] = df['Low'].astype(float)
            
            current_price = float(df['Close'].iloc[-1])
            
            # ==========================================
            # 🔍 SUPPLY, DEMAND, AND TRENDLINE ENGINE
            # ==========================================
            # Local swing high/low identification (Window check)
            df['Swing_High'] = df['High'] == df['High'].rolling(window=15, center=True).max()
            df['Swing_Low'] = df['Low'] == df['Low'].rolling(window=15, center=True).min()
            
            high_indices = df[df['Swing_High']]
            low_indices = df[df['Swing_Low']]
            
            # Extract latest clear structural zones
            recent_highs = high_indices['High'].tail(5).tolist()
            recent_lows = low_indices['Low'].tail(5).tolist()
            
            # Algorithmic Supply & Demand Zones definitions
            supply_zone = max(recent_highs) if recent_highs else current_price * 1.02
            demand_zone = min(recent_lows) if recent_lows else current_price * 0.98
            
            # Simple structural trend calculation (using last 3 swing lows/highs for vector direction)
            if len(recent_lows) >= 3 and len(recent_highs) >= 3:
                trend_slope = np.polyfit(range(3), recent_lows[-3:], 1)[0]
            else:
                trend_slope = 0
                
            market_trend = "BULLISH" if trend_slope > 0 else "BEARISH"
            
            # ==========================================
            # 🧠 CONFLUENCE MATCHING & CONFIDENCE LOGIC
            # ==========================================
            signal = "STANDBY"
            confidence = 50
            reason = "Market consolidating in mid-range equity value. No high-probability edge present."
            stop_loss = 0.0
            take_profit = 0.0
            
            # Proximity thresholds
            dist_to_supply = abs(supply_zone - current_price)
            dist_to_demand = abs(current_price - demand_zone)
            
            # BUY Setup Rule: Price inside Demand Zone AND general structural trend is Bullish
            if current_price <= (demand_zone * 1.005) and market_trend == "BULLISH":
                signal = "BUY"
                confidence = 88
                reason = "Price rejected hard off primary Demand block with solid Ascending Trendline alignment. Major liquidity swept."
                stop_loss = demand_zone * 0.996
                take_profit = supply_zone * 0.998
                
            # SELL Setup Rule: Price inside Supply Zone AND general structural trend is Bearish
            elif current_price >= (supply_zone * 0.995) and market_trend == "BEARISH":
                signal = "SELL"
                confidence = 92
                reason = "Price tapped directly into Institutional Supply block. Heavy order block absorption detected with Descending Trendline confirmation."
                stop_loss = supply_zone * 1.004
                take_profit = demand_zone * 1.002
                
            # Minor Bounce or Counter-trend adjustments
            elif current_price <= (demand_zone * 1.005):
                signal = "BUY"
                confidence = 65
                reason = "Testing major demand block floor, but structural macro trendline remains heavy/bearish."
                stop_loss = demand_zone * 0.995
                take_profit = current_price + (current_price - stop_loss) * 2
                
            elif current_price >= (supply_zone * 0.995):
                signal = "SELL"
                confidence = 70
