import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import google.generativeai as genai
from PIL import Image

# ==========================================
# ❄️ GLOBAL TERMINAL THEME INJECTION
# ==========================================
st.set_page_config(page_title="Carnage Terminal v6.0 Vision", page_icon="❄️", layout="wide")

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
st.markdown("<h1 style='text-align: center;'>❄️ CARNAGE VISION TERMINAL V6.0 ❄️</h1>", unsafe_allow_html=True)
st.write("---")

# ==========================================
# 🎛️ SIDEBAR CONFIGURATION (SECURITY KEYS)
# ==========================================
st.sidebar.markdown("### 🔑 SECURITY HUB")
vision_api_key = st.sidebar.text_input("CARNAGE VISION API KEY:", type="password", help="Get a free key from Google AI Studio")

# ==========================================
# 🧭 MAIN NAVIGATION MATRIX (TABS)
# ==========================================
tab_vision, tab_api = st.tabs(["⚡ AI CHART VISION SNIPER", "📊 DELAYED DATA ALGO MATRIX"])

# ------------------------------------------
# TAB 1: AI CHART VISION SNIPER ENGINE
# ------------------------------------------
with tab_vision:
    st.markdown("### 📸 Visual Chart Analysis Engine")
    st.write("Upload a direct screenshot of your live MT5 chart. The terminal will read your broker price visually and analyze structural setups.")
    
    if not vision_api_key:
        st.warning("⚠️ Please paste your free Vision API Key in the left sidebar to unlock the chart uploader matrix.")
    else:
        # Initialize Gemini Vision Configuration
        genai.configure(api_key=vision_api_key)
        
        uploaded_chart = st.file_uploader("📥 DROP MT5 CHART SCREENSHOT HERE:", type=["png", "jpg", "jpeg"])
        
        col_v1, col_v2 = st.columns([1, 1])
        
        with col_v1:
            account_cap = st.number_input("💰 CAPITALIZATION ($):", value=1000.0, step=100.0, key="vision_cap")
            risk_pct = st.slider("⚖️ PER-TRADE RISK %:", min_value=0.5, max_value=5.0, value=2.0, step=0.5)
            
        with col_v2:
            if uploaded_chart:
                st.image(uploaded_chart, caption="Uploaded Live Broker Feed", use_container_width=True)
        
        if uploaded_chart and st.button("🧊 EXECUTE COGNITIVE VISUAL ANALYSIS"):
            with st.spinner("❄️ Initiating Carnage Vision Engine... Reading exact broker digits and structural ranges..."):
                try:
                    img = Image.open(uploaded_chart)
                    
                    analysis_prompt = f"""
                    You are the advanced institutional vision analysis module of the Carnage Trading Terminal. 
                    Analyze this uploaded trading chart screenshot with extreme technical precision.
                    
                    Tasks:
                    1. Read the absolute current live price displayed on the right-hand axis or price tags.
                    2. Identify the active market structure (Bullish, Bearish, or Ranging).
                    3. Check for Smart Money Concepts (SMC): Look for recent Liquidity Sweeps (Fakeouts below old floors/ceilings) or Market Structure Shifts (CHoCH/Displacement).
                    4. Based on your visual assessment, issue a definitive trading signal: BUY, SELL, or STANDBY.
                    5. If a signal is issued, calculate a highly accurate structural Stop Loss (SL) and Take Profit (TP) matching the exact price numbers on this specific broker chart.
                    
                    Account Balance: ${{account_cap}}
                    Risk Percentage: {risk_pct}%
                    
                    Format your response strictly using this clean markdown template so it renders cleanly inside our UI layout:
                    
                    ### 📊 VISUAL DETECTOR STATUS
                    * **Detected Live Broker Price:** [Insert precise price found on chart]
                    * **Visual Market Structure:** [Bullish/Bearish/Consolidating]
                    * **SMC Footprint Event:** [e.g., Bullish Liquidity Sweep / Order Block Mitigation / None]
                    
                    ### ⚡ STRATEGIC SIGNAL OUTPUT: [BUY, SELL, or STANDBY]
                    * **Logic & Reasoning:** [Provide a high-tier professional analysis breakdown explaining exactly what you saw in the candle shapes and levels]
                    
                    ### 🎯 TARGET EXECUTION PROTECTION MATRIX
                    | Metric | Target Value |
                    | :--- | :--- |
                    | **⚡ EXACT ENTRY PRICE** | [Insert live chart price] |
                    | **🛑 STRUCTURE ACCURATE STOP LOSS (SL)** | [Insert calculated chart price] |
                    | **🟢 STRUCTURE ACCURATE TAKE PROFIT (TP)** | [Insert calculated chart price] |
                    | **⚖️ CALCULATED LOT SIZE** | [Calculate standard lot sizing using standard contract specifications for this asset given a risk amount of {account_cap * (risk_pct/100)}] |
                    """
                    
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    response = model.generate_content([analysis_prompt, img])
                    
                    st.write("---")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"❌ Structural Processing Error: {str(e)}")

# ------------------------------------------
# TAB 2: TRADITIONAL DATA MATRIX (ALGORITHMS)
# ------------------------------------------
with tab_api:
    st.markdown("### 📊 Delayed API Matrix Feed")
    st.write("Fallback structural scanners running on public stock exchange pipelines.")
    
    # Global Controls for Data Matrix
    col_ui1, col_ui2, col_ui3 = st.columns(3)
    with col_ui1:
        asset_options = ["GOLD (XAUUSD)", "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD"]
        selected_asset = st.selectbox("💱 TARGET ASSET BLOCK:", asset_options)
        account_balance = st.number_input("💰 ACCOUNT CAPITALIZATION ($):", value=1000.0, step=100.0, key="api_cap")
    
    with col_ui2:
        timeframe_options = ["M5 (5m)", "M15 (15m)", "H1 (1h)", "H4 (4h)", "D1 (Daily)"]
        selected_tf = st.selectbox("⏳ RUNTIME TIMEFRAME:", timeframe_options)
        
    with col_ui3:
        mt5_live_price = st.number_input("📲 LIVE MT5 PRICE SYNC OVERRIDE:", value=0.0, step=0.01)

    # Core Logic Setup
    ticker_map = {"GOLD (XAUUSD)": "GC=F", "EURUSD": "EURUSD=X", "GBPUSD": "GBPUSD=X", "USDJPY": "JPY=X", "AUDUSD": "AUDUSD=X", "USDCAD": "USDCAD=X"}
    target_ticker = ticker_map[selected_asset]
    
    if "M5" in selected_tf: tf_interval, tf_period, lookback_bars = "5m", "5d", 100
    elif "M15" in selected_tf: tf_interval, tf_period, lookback_bars = "15m", "1mo", 100
    elif "H1" in selected_tf: tf_interval, tf_period, lookback_bars = "1h", "1mo", 48
    else: tf_interval, tf_period, lookback_bars = "1h", "3mo", 50

    def fetch_processed_data():
        df = yf.Ticker(target_ticker).history(period=tf_period, interval=tf_interval)
        if not df.empty and "H4" in selected_tf:
            df = df.resample('4H').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'}).dropna()
        return df

    sub_v4, sub_v5 = st.tabs(["🧬 RETAIL PULLBACK (V4)", "🏛️ INSTITUTIONAL SMC (V5)"])
    
    # V4 Math Layer
    with sub_v4:
        if st.button("🧊 RUN ALGO MATRICES (V4)"):
            df = fetch_processed_data()
            if df.empty or len(df) < lookback_bars:
                st.error("⚠️ Sync limitations hit.")
            else:
                df['Close'] = df['Close'].astype(float)
                current_price = float(df['Close'].iloc[-1])
                recent_data = df.tail(lookback_bars)
                
                fib_high = float(recent_data['High'].max())
                fib_low = float(recent_data['Low'].min())
                fib_range = (fib_high - fib_low) if (fib_high - fib_low) > 0 else 0.0001
                fib_500 = fib_high - (0.500 * fib_range)
                
                stop_loss = fib_low if current_price > fib_500 else fib_high
                take_profit = fib_high if current_price > fib_500 else fib_low
                signal = "BUY" if current_price > fib_500 else "SELL"
                
                if mt5_live_price > 0:
                    exec_entry, exec_sl, exec_tp = mt5_live_price, mt5_live_price - abs(current_price - stop_loss), mt5_live_price + abs(current_price - take_profit)
                else:
                    exec_entry, exec_sl, exec_tp = current_price, stop_loss, take_profit
                    
                st.metric("⚡ SIGNAL", signal)
                o1, o2, o3 = st.columns(3)
                o1.metric("ENTRY", f"{exec_entry:.2f}")
                o2.metric("SL", f"{exec_sl:.2f}")
                o3.metric("TP", f"{exec_tp:.2f}")

    # V5 Math Layer
    with sub_v5:
        if st.button("🧊 RUN INSTI-SMC SCAN (V5)"):
            df = fetch_processed_data()
            if df.empty or len(df) < lookback_bars:
                st.error("⚠️ Data connection sync issue.")
            else:
                df['Close'] = df['Close'].astype(float)
                current_price = float(df['Close'].iloc[-1])
                prior_high = float(df['High'].tail(25).max())
                prior_low = float(df['Low'].tail(25).min())
                
                signal = "BUY" if current_price > prior_low else "SELL"
                stop_loss = current_price - 4.5 if signal == "BUY" else current_price + 4.5
                take_profit = prior_high if signal == "BUY" else prior_low
                
                if mt5_live_price > 0:
                    exec_entry, exec_sl, exec_tp = mt5_live_price, mt5_live_price - abs(current_price - stop_loss), mt5_live_price + abs(current_price - take_profit)
                else:
                    exec_entry, exec_sl, exec_tp = current_price, stop_loss, take_profit
                    
                st.metric("🏛️ SMC SIGNAL", signal)
                oo1, oo2, oo3 = st.columns(3)
                oo1.metric("ENTRY", f"{exec_entry:.2f}")
                oo2.metric("SL", f"{exec_sl:.2f}")
                oo3.metric("TP", f"{exec_tp:.2f}")
