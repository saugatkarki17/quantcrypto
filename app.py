import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page Config Streamlit
st.set_page_config(page_title="Crypto Alpha Hunter", layout="wide", page_icon="🦈")

# STYLING
st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    h1, h2, h3 { color: #00F0FF !important; font-family: 'Helvetica', sans-serif; }
    .stMetric { background-color: #1f2937; border: 1px solid #374151; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# SIDEBAR FOR CRYPTO SELECTION
st.sidebar.header("Market Scanner")
# Default list of major assets to compare
default_tickers = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'BNB-USD', 'XRP-USD', 'ADA-USD', 'MATIC-USD', 'DOGE-USD']
tickers = st.sidebar.multiselect("Select Assets to Correlate", default_tickers, default=default_tickers[:4])
lookback = st.sidebar.slider("Lookback Period (Days)", 30, 365, 90)
window = st.sidebar.slider("Rolling Correlation Window", 7, 60, 30)

st.title("Crypto Decoupling Detector")
st.markdown("### Finding 'Uncorrelated Alpha' in a uncertain public sentiment")

# DATA ENGINE
@st.cache_data
def get_data(tickers, period="2y"):
    data = yf.download(tickers, period=period)['Close']
    return data

if len(tickers) < 2:
    st.error("Please select at least 2 assets to analyze correlation.")
else:
    try:
        with st.spinner('Fetching live market data...'):
            # Download Data
            df = get_data(tickers)
            
            # Calculate Returns
            returns = df.pct_change().dropna()
            
            # Cumulative Returns (for the first chart)
            cum_returns = (1 + returns).cumprod()

        # KPI 
        # We assume the first ticker selected is the "Benchmark" (usually BTC)
        benchmark = tickers[0]
        st.write(f"**Benchmark Analysis:** Correlation vs {benchmark} (Last {window} Days)")
        
        cols = st.columns(len(tickers)-1)
        for i, tick in enumerate(tickers[1:]):
            # Calculate rolling correlation
            rolling_corr = returns[benchmark].rolling(window=window).corr(returns[tick])
            current_corr = rolling_corr.iloc[-1]
            
            # Color logic: Low correlation is GOOD (Green), High is BAD (Red)
            delta_color = "normal" 
            if current_corr > 0.8: 
                state = "Lockstep"
            elif current_corr < 0.5:
                state = "Decoupled (Alpha?)"
            else:
                state = "Linked"
                
            with cols[i % len(cols)]:
                st.metric(
                    label=f"{tick}", 
                    value=f"{current_corr:.2f}", 
                    delta=state,
                    delta_color="off" # Handle color via logic if needed, but standard is fine
                )

        # --- TABBED ANALYSIS ---
        tab1, tab2, tab3 = st.tabs(["Performance", "Rolling Correlation", "Heatmap Matrix"])

        with tab1:
            st.subheader("Normalized Performance Comparison")
            # Normalize to start at 100 for fair comparison
            normalized_df = df / df.iloc[0] * 100
            
            fig_perf = px.line(normalized_df, x=normalized_df.index, y=normalized_df.columns, 
                               title="Asset Growth (Base 100)", template="plotly_dark")
            fig_perf.update_yaxes(title="Growth ($100 invested)")
            st.plotly_chart(fig_perf, use_container_width=True)

        with tab2:
            st.subheader(f"Dynamic Rolling Correlation vs {benchmark}")
            st.caption(f"How much do these assets mimic {benchmark}? Lower is better for diversification.")
            
            corr_df = pd.DataFrame()
            for tick in tickers:
                if tick != benchmark:
                    corr_df[tick] = returns[benchmark].rolling(window=window).corr(returns[tick])
            
            fig_roll = px.line(corr_df, title=f"{window}-Day Rolling Correlation to {benchmark}", template="plotly_dark")
            
            # "Danger Zone" shading for high correlation
            fig_roll.add_hrect(y0=0.8, y1=1.0, line_width=0, fillcolor="red", opacity=0.1, annotation_text="Danger Zone (Contagion)")
            fig_roll.add_hrect(y0=-1.0, y1=0.3, line_width=0, fillcolor="green", opacity=0.1, annotation_text="Alpha Zone (Decoupled)")
            
            fig_roll.update_yaxes(range=[-1, 1])
            st.plotly_chart(fig_roll, use_container_width=True)

        with tab3:
            st.subheader("Current Market Correlation Matrix")
            # Correlation matrix of the last 'window' days
            recent_corr = returns.tail(window).corr()
            
            fig_heat = px.imshow(
                recent_corr, 
                text_auto=True, 
                aspect="auto", 
                color_continuous_scale="RdBu_r", # Red = High Corr, Blue = Inverse
                zmin=-1, zmax=1,
                template="plotly_dark",
                title=f"Correlation Matrix (Last {window} Days)"
            )
            st.plotly_chart(fig_heat, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")