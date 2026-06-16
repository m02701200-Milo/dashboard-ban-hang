import streamlit as st
from utils.data_loader import load_data
from utils.style import load_css
from pages import dashboard, products, orders, analysis, export

st.set_page_config(
    page_title="Dashboard Bán hàng Điện tử",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

products_df, orders_df = load_data()

# sidebar điều hướng
with st.sidebar:
    st.markdown("## 🛒 Quản lý Bán hàng")
    st.markdown("---")
    menu = st.radio(
        "nav",
        ["📊 Tổng quan", "📦 Quản lý Sản phẩm", "🧾 Đơn hàng", "📈 Phân tích", "📤 Xuất báo cáo"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("**Thống kê nhanh**")
    don_hoan_thanh = orders_df[orders_df["trang_thai_don"] == "Hoàn thành"]
    st.metric("Đơn hoàn thành", f"{len(don_hoan_thanh):,}")
    st.metric("Tổng sản phẩm", f"{len(products_df):,}")
    st.markdown("---")
    st.caption("📅 Dữ liệu: Năm 2024")

# điều hướng sang trang tương ứng
if menu == "📊 Tổng quan":
    dashboard.show(orders_df)

elif menu == "📦 Quản lý Sản phẩm":
    products.show()

elif menu == "🧾 Đơn hàng":
    orders.show(orders_df)

elif menu == "📈 Phân tích":
    analysis.show(orders_df)

elif menu == "📤 Xuất báo cáo":
    export.show(products_df, orders_df)
