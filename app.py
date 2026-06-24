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
    .stApp {
        background: linear-gradient(135deg, #050b11 0%, #091320 50%, #050a0f 100%);
        color: #e2e8f0;
    }
    h1, h2, h3 {
        color: #a5f3fc !important;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 15px rgba(165, 243, 252, 0.4);
        font-weight: 800;
    }
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(10, 23, 39, 0.75);
        border: 1px solid rgba(165, 243, 252, 0.15);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }
    button[data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-size: 16px !important;
        font-family: monospace !important;
        font-weight: bold !important;
    }
    button[aria-selected="true"] {
        color: #38bdf8 !important;
        border-bottom-color: #38bdf8 !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #0f172a 0%, #0284c7 100%) !important;
        color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 6px !important;
        font-weight: bold;
        font-size: 18px !important;
        padding: 12px 0px !important;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%) !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.7);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>❄️ CARNAGE VISION TERMINAL V6.0 ❄️</h1>", unsafe_allow_html=True)
st.write("---")

# ==========================================
# 🎛️ SIDEBAR CONFIGURATION (SECURITY KEYS)
# ==========================================
st.sidebar.
