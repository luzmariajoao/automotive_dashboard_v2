import streamlit as st
import pandas as pd
import plotly.express as px
from anthropic import Anthropic

# PAGE CONFIG
st.set_page_config(
    page_title="EU Automotive Market Intelligence",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# THEME
st.markdown("""
<style>
    :root {
        --blue: #0B2545;
        --teal: #0F9B8E;
        --coral: #C0392B;
    }
    h1, h2 { color: var(--blue); }
    .metric-card { 
        background: linear-gradient(135deg, var(--blue) 0%, var(--teal) 100%);
        color: white; padding: 20px; border-radius: 8px; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════

@st.cache_data
def load_data():
    return {
        "eu_2025": 13_270_000,
        "pt_2025": 225_039,
        "bev_2025": 17.4,
        "top_model": "Dacia Sandero",
        "top_units": 185_000,
    }

@st.cache_data
def load_brands():
    return pd.DataFrame({
        "Brand": ["Tesla", "BYD", "Volkswagen", "BMW"],
        "2025": [789_200, 1_574_000, 762_100, 371_800],
        "Growth": [-26.6, 170.0, -2.3, -4.5],
    })

# ═══════════════════════════════════════════════════════════════════
# AI CHAT
# ═══════════════════════════════════════════════════════════════════

def chat_with_ai(query):
    """Call Claude API"""
    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY")
        if not api_key:
            return "⚠️ API key not configured"
        
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=300,
            messages=[{"role": "user", "content": query}]
        )
        return response.content[0].text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ═══════════════════════════════════════════════════════════════════
# UI
# ═══════════════════════════════════════════════════════════════════

st.title("🚗 EU Automotive Market Intelligence")

# Chat
st.subheader("🔍 Ask the Market")
user_query = st.text_input("What would you like to know about the EU automotive market?")

if user_query:
    response = chat_with_ai(user_query)
    st.info(response)

st.markdown("---")

# KPIs
st.subheader("📊 Key Metrics")
data = load_data()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div style='font-size: 24px; font-weight: 700;'>13.27M</div>
        <div style='font-size: 12px;'>EU 2025 Registrations</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div style='font-size: 24px; font-weight: 700;'>225K</div>
        <div style='font-size: 12px;'>Portugal 2025</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div style='font-size: 24px; font-weight: 700;'>17.4%</div>
        <div style='font-size: 12px;'>BEV Share</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div style='font-size: 24px; font-weight: 700;'>Sandero</div>
        <div style='font-size: 12px;'>#1 Model</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Chart
st.subheader("🏆 Top Brands")
brands = load_brands()
fig = px.bar(brands, x="Brand", y="2025", color_discrete_sequence=["#0B2545"])
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("📋 Data: ACEA, JATO Dynamics | Last updated: 2026-Q1")
