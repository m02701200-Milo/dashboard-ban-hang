import streamlit as st

def load_css():
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        }
        [data-testid="stSidebar"] * {
            color: #e0e0e0 !important;
        }

        .kpi-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            padding: 20px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            margin-bottom: 10px;
        }
        .kpi-card.green  { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
        .kpi-card.orange { background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%); }
        .kpi-card.red    { background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%); }
        .kpi-card.blue   { background: linear-gradient(135deg, #4776e6 0%, #8e54e9 100%); }
        .kpi-number { font-size: 28px; font-weight: 700; margin: 8px 0; }
        .kpi-label  { font-size: 13px; opacity: 0.9; }
        .kpi-sub    { font-size: 12px; opacity: 0.8; margin-top: 4px; }

        .page-header {
            background: linear-gradient(90deg, #1a1a2e, #0f3460);
            border-radius: 10px;
            padding: 15px 25px;
            color: white;
            margin-bottom: 20px;
        }

        footer { visibility: hidden; }

        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = ""):
    """in header có gradient cho mỗi trang"""
    st.markdown(
        f'<div class="page-header">'
        f'<h2 style="margin:0">{title}</h2>'
        f'<p style="margin:4px 0 0;opacity:.8">{subtitle}</p>'
        f'</div>',
        unsafe_allow_html=True
    )


def kpi_card(label: str, value: str, sub: str = "", color: str = "blue"):
    return f"""
    <div class="kpi-card {color}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-number">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>"""
