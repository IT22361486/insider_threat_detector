# src/dashboard.py - FINAL APPROVED VERSION
import streamlit as st
import pandas as pd
import joblib
import time
from datetime import datetime
import plotly.express as px
import base64
import os

# ========== Enhanced Dark Mode Setup ==========
def set_dark_mode():
    st.markdown("""
    <style>
    :root {
        --primary-bg: #121212;
        --secondary-bg: #1e1e1e;
        --card-bg: #2d2d2d;
        --text-color: #ffffff;
        --accent-color: #4e8cff;
        --warning-color: #ffc107;
        --critical-color: #dc3545;
        --normal-color: #28a745;
        --border-color: #444;
    }
    
    .stApp {
        background-color: var(--primary-bg);
        color: var(--text-color);
    }
    
    .stSidebar {
        background-color: var(--secondary-bg) !important;
        border-right: 1px solid var(--border-color);
    }
    
    .header-container {
        display: flex;
        align-items: center;
        background-color: var(--secondary-bg);
        padding: 15px 25px;
        border-radius: 8px;
        margin-bottom: 25px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.2);
        border-bottom: 1px solid var(--border-color);
    }
    
    .header-banner {
        height: 50px;
        width: auto;
        max-width: 100%;
    }
    
    /* Rest of your existing CSS remains unchanged */
    </style>
    """, unsafe_allow_html=True)

# ========== Image Handling ==========
def get_image_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
        return None

def show_images():
    banner_path = "assets/banner.png"
    
    if not os.path.exists(banner_path):
        st.error(f"Banner not found at: {os.path.abspath(banner_path)}")
        return
    
    banner_base64 = get_image_base64(banner_path)
    
    if banner_base64:
        st.markdown(f"""
        <div class="header-container">
            <img class="header-banner" src="data:image/png;base64,{banner_base64}">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Banner image not loaded - using text header instead")
        st.title("Insider Threat Dashboard")

# ========== Page Config ==========
st.set_page_config(
    layout="wide",
    page_title="Insider Threat Dashboard",
    page_icon="assets/logo.png"
)

# ========== Sidebar Controls ==========
with st.sidebar:
    dark_mode = st.checkbox("Dark Mode", value=True)
    if dark_mode:
        set_dark_mode()
    
    st.image("assets/logo.png", width=60)
    st.title("Controls")
    refresh_rate = st.slider("Refresh Rate (seconds)", 1, 10, 3)
    min_threat = st.selectbox("Minimum Alert Level", ["Warning (1+)", "Critical (2)"])
    st.markdown("---")
    st.caption(f"Last Model Training: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# ========== Main Dashboard ==========
show_images()

try:
    data = pd.read_csv("data/processed/final_features_labeled.csv")
    model = joblib.load("data/results/threat_model.pkl")
except FileNotFoundError as e:
    st.error(f"Missing file: {str(e)}\n\nRun train_model.py first!")
    st.stop()

# Convert selection to numeric
threat_filter = 1 if "Warning" in min_threat else 2

# Real-time monitoring
if st.button("▶️ Start Live Monitoring", type="primary", key="start_monitoring"):
    placeholder = st.empty()
    stop_monitoring = False
    
    while not stop_monitoring:
        filtered_data = data[data['threat_level'] >= threat_filter]
        sample = filtered_data.sample(3) if len(filtered_data) > 0 else data.sample(3)
        
        with placeholder.container():
            # Current threats
            st.subheader("🔍 Live Threat Detection")
            
            cols = st.columns(3)
            for i, (_, row) in enumerate(sample.iterrows()):
                threat_class = {
                    0: "normal",
                    1: "warning",
                    2: "critical"
                }[row['threat_level']]
                
                with cols[i]:
                    st.markdown(
                        f"""
                        <div class="threat-card {threat_class}">
                            <h4 style="color: {'var(--normal-color)' if threat_class=='normal' else 'var(--warning-color)' if threat_class=='warning' else 'var(--critical-color)'}; 
                                       margin-top: 0; margin-bottom: 10px;">{row['user']}</h4>
                            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                                <div>Logins: <strong>{row['logins_per_day']}</strong></div>
                                <div>Devices: <strong>{int(row['device_connections'])}</strong></div>
                            </div>
                            <p style="color: {'var(--normal-color)' if threat_class=='normal' else 'var(--warning-color)' if threat_class=='warning' else 'var(--critical-color)'}; 
                                      font-weight: bold; margin-top: 12px; margin-bottom: 0;">
                                {'✅ Normal' if threat_class=='normal' else '⚠️ Warning' if threat_class=='warning' else '🚨 CRITICAL'}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            # Historical trends
            st.markdown("---")
            st.subheader("📈 Threat Trend Analysis")
            
            daily_threats = data.groupby('date')['threat_level'].mean().reset_index()
            fig = px.line(
                daily_threats,
                x='date',
                y='threat_level',
                color_discrete_sequence=['var(--accent-color)'],
                height=300
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=30, b=20),
                font=dict(color='white'),
                xaxis=dict(gridcolor='var(--border-color)'),
                yaxis=dict(gridcolor='var(--border-color)'),
                hoverlabel=dict(
                    bgcolor='var(--card-bg)',
                    font_size=12,
                    font_color='white'
                )
            )
            st.plotly_chart(fig, use_container_width=True, key=f"threat_trend_{time.time()}")
            
            # Threat index
            current_threat = daily_threats['threat_level'].iloc[-1]
            delta = daily_threats['threat_level'].diff().iloc[-1]
            st.metric(
                label="Current Threat Index",
                value=f"{current_threat:.1f}",
                delta=f"{delta:.1f} from yesterday",
                delta_color="inverse"
            )
            
            # Alert log
            st.markdown("---")
            st.subheader("📋 Recent Alerts")
            st.dataframe(
                sample[['user', 'date', 'logins_per_day', 'device_connections', 'threat_level']],
                column_config={
                    "threat_level": st.column_config.ProgressColumn(
                        "Threat Level",
                        help="0=Normal, 1=Warning, 2=Critical",
                        format="%d",
                        min_value=0,
                        max_value=2,
                    )
                },
                hide_index=True,
                use_container_width=True,
                key=f"alert_table_{time.time()}"
            )
            
            if st.button("⏹️ Stop Monitoring", type="secondary", key=f"stop_{time.time()}"):
                stop_monitoring = True
                placeholder.empty()
                st.success("Monitoring stopped")
                break
        
        time.sleep(refresh_rate)