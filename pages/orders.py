import streamlit as st
from utils.style import page_header


def show(orders_df):
    page_header("🧾 Quản lý Đơn hàng", "Tra cứu và lọc toàn bộ đơn hàng")

    with st.expander("🔍 Bộ lọc", expanded=True):
        cf1, cf2, cf3, cf4 = st.columns(4)
        with cf1:
            f_trang_thai = st.multiselect("Trạng thái",
                orders_df["trang_thai_don"].unique().tolist(),
                default=orders_df["trang_thai_don"].unique().tolist())
        with cf2:
            f_danh_muc = st.multiselect("Danh mục",
                orders_df["danh_muc"].unique().tolist(),
                default=orders_df["danh_muc"].unique().tolist())
        with cf3:
            f_tinh = st.multiselect("Tỉnh/Thành",
                orders_df["tinh_thanh"].unique().tolist(),
                default=orders_df["tinh_thanh"].unique().tolist())
        with cf4:
            f_thang = st.slider("Tháng", 1, 12, (1, 12))

        f_search = st.text_input("🔍 Tìm theo tên khách hàng / mã đơn", placeholder="Nhập tên hoặc mã đơn...")

    filtered = orders_df[
        (orders_df["trang_thai_don"].isin(f_trang_thai)) &
        (orders_df["danh_muc"].isin(f_danh_muc)) &
        (orders_df["tinh_thanh"].isin(f_tinh)) &
        (orders_df["thang"].between(f_thang[0], f_thang[1]))
    ]
    if f_search:
        filtered = filtered[
            filtered["khach_hang"].str.contains(f_search, case=False, na=False) |
            filtered["ma_don_hang"].str.contains(f_search, case=False, na=False)
        ]

    k1, k2, k3 = st.columns(3)
    k1.metric("Số đơn", f"{len(filtered):,}")
    k2.metric("Doanh thu", f"{filtered['thanh_tien'].sum()/1e6:.1f}M đ")
    k3.metric("Tổng SL", f"{filtered['so_luong'].sum():,}")

    show_cols = ["ma_don_hang", "ngay_dat", "ten_san_pham", "danh_muc",
                 "khach_hang", "tinh_thanh", "so_luong", "don_gia",
                 "thanh_tien", "phuong_thuc_tt", "trang_thai_don"]
    show_df = filtered[show_cols].copy()
    show_df["don_gia"]    = show_df["don_gia"].apply(lambda x: f"{x:,.0f} đ")
    show_df["thanh_tien"] = show_df["thanh_tien"].apply(lambda x: f"{x:,.0f} đ")
    show_df["ngay_dat"]   = show_df["ngay_dat"].dt.strftime("%d/%m/%Y")

    st.dataframe(show_df, use_container_width=True, height=500)
