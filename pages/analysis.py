import streamlit as st
import plotly.express as px
from utils.style import page_header


def show(orders_df):
    page_header("📈 Phân tích chuyên sâu", "Xu hướng và insight từ dữ liệu")

    tab_a, tab_b, tab_c = st.tabs(["📅 Theo thời gian", "🏷️ Theo danh mục", "💡 Insight"])

    don_ht = orders_df[orders_df["trang_thai_don"] == "Hoàn thành"]

    with tab_a:
        _bieu_do_thoi_gian(don_ht)

    with tab_b:
        _bieu_do_danh_muc(don_ht, orders_df)

    with tab_c:
        _insight(don_ht, orders_df)


def _bieu_do_thoi_gian(don_ht):
    col_ctrl, col_chart = st.columns([1, 3])
    with col_ctrl:
        loai = st.radio("Xem theo", ["Doanh thu", "Số đơn hàng", "Lợi nhuận"])
        don_vi = st.radio("Đơn vị", ["Tháng", "Quý"])

    with col_chart:
        if don_vi == "Tháng":
            don_ht_g = don_ht.copy()
            don_ht_g["label"] = don_ht_g["thang"].apply(lambda x: f"T{x:02d}")
        else:
            don_ht_g = don_ht.copy()
            don_ht_g["label"] = don_ht_g["quy"].apply(lambda x: f"Q{x}")

        if loai == "Doanh thu":
            agg = don_ht_g.groupby("label")["thanh_tien"].sum().reset_index()
            agg.columns = ["label", "Giá trị"]
            y_title = "VNĐ"
        elif loai == "Số đơn hàng":
            agg = don_ht_g.groupby("label").size().reset_index(name="Giá trị")
            y_title = "Đơn hàng"
        else:
            agg = don_ht_g.groupby("label")["loi_nhuan"].sum().reset_index()
            agg.columns = ["label", "Giá trị"]
            y_title = "VNĐ"

        fig = px.line(agg, x="label", y="Giá trị",
                      markers=True, line_shape="spline",
                      color_discrete_sequence=["#667eea"],
                      title=f"{loai} theo {don_vi.lower()}")
        fig.update_traces(line_width=3, marker_size=8)
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                          yaxis_title=y_title, height=380, xaxis_title=don_vi)
        st.plotly_chart(fig, use_container_width=True)


def _bieu_do_danh_muc(don_ht, orders_df):
    #slider để lọc theo khoảng giá — kéo qua lại xem biểu đồ thay đổi
    gia_min = int(orders_df["don_gia"].min())
    gia_max = int(orders_df["don_gia"].max())
    gia_range = st.slider("💰 Lọc theo khoảng giá (VNĐ)",
                          gia_min, gia_max, (gia_min, gia_max),
                          step=500000, format="%d đ")

    loc_gia = don_ht[(don_ht["don_gia"] >= gia_range[0]) & (don_ht["don_gia"] <= gia_range[1])]

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        dt_dm = loc_gia.groupby("danh_muc")["thanh_tien"].sum().sort_values(ascending=False).reset_index()
        dt_dm.columns = ["Danh mục", "Doanh thu"]
        fig_dm = px.bar(dt_dm, x="Danh mục", y="Doanh thu", color="Danh mục",
                        text=dt_dm["Doanh thu"].apply(lambda x: f"{x/1e6:.0f}M"),
                        title="Doanh thu theo danh mục")
        fig_dm.update_traces(textposition="outside")
        fig_dm.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                              showlegend=False, height=380)
        st.plotly_chart(fig_dm, use_container_width=True)

    with col_b2:
        sp_ban = loc_gia.groupby("danh_muc")["so_luong"].sum().sort_values(ascending=False).reset_index()
        sp_ban.columns = ["Danh mục", "Số lượng bán"]
        fig_sp = px.pie(sp_ban, values="Số lượng bán", names="Danh mục",
                        hole=0.4, title="Tỉ lệ số lượng bán theo danh mục",
                        color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_sp.update_layout(height=380, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_sp, use_container_width=True)

    # Scatter xem sản phẩm nào giá cao mà vẫn bán được nhiều
    st.subheader("🔵 Giá bán vs Số lượng bán ra")
    scatter_data = loc_gia.groupby("ten_san_pham").agg(
        so_luong=("so_luong", "sum"),
        doanh_thu=("thanh_tien", "sum"),
        gia_tb=("don_gia", "mean"),
        danh_muc=("danh_muc", "first")
    ).reset_index()

    fig_sc = px.scatter(scatter_data, x="gia_tb", y="so_luong",
                        color="danh_muc", size="doanh_thu",
                        hover_name="ten_san_pham",
                        labels={"gia_tb": "Giá TB (đ)", "so_luong": "Số lượng bán"},
                        color_discrete_sequence=px.colors.qualitative.Set2)
    fig_sc.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", height=420)
    st.plotly_chart(fig_sc, use_container_width=True)


def _insight(don_ht, orders_df):
    st.subheader("💡 Insight")

    i1, i2 = st.columns(2)
    with i1:
        pt_tt = don_ht["phuong_thuc_tt"].value_counts().reset_index()
        pt_tt.columns = ["Phương thức", "Số đơn"]
        fig_pt = px.bar(pt_tt, x="Phương thức", y="Số đơn",
                        color="Phương thức", text="Số đơn",
                        title="Khách hay dùng phương thức thanh toán nào?")
        fig_pt.update_traces(textposition="outside")
        fig_pt.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                              showlegend=False, height=350)
        st.plotly_chart(fig_pt, use_container_width=True)

    with i2:
        # tỉ lệ hủy đơn — danh mục nào cao thì cần xem lại chất lượng hoặc giá
        huy_rate = orders_df.groupby("danh_muc").apply(
            lambda x: (x["trang_thai_don"] == "Đã hủy").sum() / len(x) * 100
        ).reset_index()
        huy_rate.columns = ["Danh mục", "Tỉ lệ hủy (%)"]
        huy_rate = huy_rate.sort_values("Tỉ lệ hủy (%)", ascending=False)
        fig_huy = px.bar(huy_rate, x="Danh mục", y="Tỉ lệ hủy (%)",
                         color="Tỉ lệ hủy (%)", color_continuous_scale="Reds",
                         text=huy_rate["Tỉ lệ hủy (%)"].apply(lambda x: f"{x:.1f}%"),
                         title="Tỉ lệ hủy đơn theo danh mục")
        fig_huy.update_traces(textposition="outside")
        fig_huy.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                               coloraxis_showscale=False, height=350)
        st.plotly_chart(fig_huy, use_container_width=True)

    st.subheader("🌡️ Heatmap doanh thu: Danh mục × Tháng")
    heat_data  = don_ht.groupby(["danh_muc", "thang"])["thanh_tien"].sum().reset_index()
    heat_pivot = heat_data.pivot(index="danh_muc", columns="thang", values="thanh_tien").fillna(0)
    heat_pivot.columns = [f"T{c:02d}" for c in heat_pivot.columns]

    fig_heat = px.imshow(heat_pivot / 1e6,
                         labels=dict(color="Triệu đ"),
                         color_continuous_scale="Blues",
                         text_auto=".0f", aspect="auto")
    fig_heat.update_layout(height=320, paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_heat, use_container_width=True)
