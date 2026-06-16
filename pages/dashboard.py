import streamlit as st
import plotly.express as px
from utils.style import page_header, kpi_card


def show(orders_df):
    page_header("📊 Tổng quan kinh doanh", "Dữ liệu năm 2024 · Cập nhật mới nhất")

    don_ht = orders_df[orders_df["trang_thai_don"] == "Hoàn thành"]

    tong_doanh_thu = don_ht["thanh_tien"].sum()
    tong_loi_nhuan = don_ht["loi_nhuan"].sum()
    tong_don       = len(don_ht)
    san_pham_ban   = don_ht["so_luong"].sum()

    #thẻ KPI
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card("💰 Tổng Doanh Thu", f"{tong_doanh_thu/1e9:.2f} tỷ", "VNĐ · Đơn hoàn thành", "blue"), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card("📈 Lợi Nhuận Gộp", f"{tong_loi_nhuan/1e9:.2f} tỷ", f"Biên LN: {tong_loi_nhuan/tong_doanh_thu*100:.1f}%", "green"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card("🧾 Đơn Hoàn Thành", f"{tong_don:,}", f"Tổng {len(orders_df):,} đơn", "orange"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card("📦 Sản Phẩm Đã Bán", f"{san_pham_ban:,}", f"TB {san_pham_ban/tong_don:.1f} sp/đơn", "red"), unsafe_allow_html=True)

    st.markdown("---")

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.subheader("📅 Doanh thu theo tháng")
        dt_thang = don_ht.groupby("thang")["thanh_tien"].sum().reset_index()
        dt_thang.columns = ["Tháng", "Doanh thu"]
        dt_thang["Tháng"] = dt_thang["Tháng"].apply(lambda x: f"T{x:02d}")

        fig1 = px.bar(
            dt_thang, x="Tháng", y="Doanh thu",
            color="Doanh thu", color_continuous_scale="Blues",
            text=dt_thang["Doanh thu"].apply(lambda x: f"{x/1e6:.0f}M"),
        )
        fig1.update_traces(textposition="outside")
        fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                           coloraxis_showscale=False, height=350,
                           margin=dict(t=20, b=20), yaxis_title="VNĐ")
        st.plotly_chart(fig1, use_container_width=True)

    with col_right:
        st.subheader("🥧 Tỉ lệ theo danh mục")
        dt_danh_muc = don_ht.groupby("danh_muc")["thanh_tien"].sum().reset_index()
        fig2 = px.pie(dt_danh_muc, values="thanh_tien", names="danh_muc",
                      hole=0.45, color_discrete_sequence=px.colors.qualitative.Set3)
        fig2.update_traces(textinfo="percent+label", pull=[0.05]*len(dt_danh_muc))
        fig2.update_layout(height=350, margin=dict(t=20, b=20),
                           showlegend=False, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig2, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("🏆 Top 10 sản phẩm bán chạy")
        top_sp = (don_ht.groupby("ten_san_pham")["so_luong"]
                        .sum().sort_values(ascending=False)
                        .head(10).reset_index())
        top_sp.columns = ["Sản phẩm", "Số lượng"]
        fig3 = px.bar(top_sp.sort_values("Số lượng"), x="Số lượng", y="Sản phẩm",
                      orientation="h", color="Số lượng",
                      color_continuous_scale="Teal", text="Số lượng")
        fig3.update_traces(textposition="outside")
        fig3.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                           coloraxis_showscale=False, height=380, margin=dict(t=10, b=10))
        st.plotly_chart(fig3, use_container_width=True)

    with col_b:
        st.subheader("🗺️ Doanh thu theo tỉnh thành")
        dt_tinh = don_ht.groupby("tinh_thanh")["thanh_tien"].sum().sort_values(ascending=False).reset_index()
        dt_tinh.columns = ["Tỉnh/Thành", "Doanh thu"]
        fig4 = px.bar(dt_tinh, x="Tỉnh/Thành", y="Doanh thu",
                      color="Doanh thu", color_continuous_scale="Oranges",
                      text=dt_tinh["Doanh thu"].apply(lambda x: f"{x/1e6:.0f}M"))
        fig4.update_traces(textposition="outside")
        fig4.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                           coloraxis_showscale=False, height=380, margin=dict(t=10, b=10))
        st.plotly_chart(fig4, use_container_width=True)

    st.subheader("📋 Trạng thái đơn hàng")
    trang_thai_count = orders_df["trang_thai_don"].value_counts().reset_index()
    trang_thai_count.columns = ["Trạng thái", "Số đơn"]
    mau = {"Hoàn thành": "#2ecc71", "Đang xử lý": "#f39c12", "Đã hủy": "#e74c3c"}
    fig5 = px.bar(trang_thai_count, x="Trạng thái", y="Số đơn",
                  color="Trạng thái", color_discrete_map=mau, text="Số đơn")
    fig5.update_traces(textposition="outside")
    fig5.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                       showlegend=False, height=300, margin=dict(t=10, b=10))
    st.plotly_chart(fig5, use_container_width=True)
