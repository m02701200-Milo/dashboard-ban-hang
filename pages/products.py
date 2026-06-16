import streamlit as st
import pandas as pd
from utils.style import page_header
from utils.data_loader import reload_products, save_products

DM_OPTIONS = ["Điện thoại", "Tai nghe", "Loa", "Tablet", "Phụ kiện", "Đồng hồ thông minh"]


def show():
    page_header("📦 Quản lý Sản phẩm", "Thêm · Sửa · Xóa sản phẩm trong kho")

    sp_df = reload_products()

    tab1, tab2, tab3 = st.tabs(["📋 Danh sách", "➕ Thêm mới", "✏️ Sửa / Xóa"])

    with tab1:
        _tab_danh_sach(sp_df)

    with tab2:
        _tab_them_moi(sp_df)

    with tab3:
        _tab_sua_xoa(sp_df)


def _tab_danh_sach(sp_df):
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filter_dm = st.selectbox("Danh mục", ["Tất cả"] + sorted(sp_df["danh_muc"].unique().tolist()))
    with col_f2:
        filter_brand = st.selectbox("Thương hiệu", ["Tất cả"] + sorted(sp_df["thuong_hieu"].unique().tolist()))
    with col_f3:
        search = st.text_input("🔍 Tìm tên sản phẩm", placeholder="Gõ tên...")

    hien_thi = sp_df.copy()
    if filter_dm != "Tất cả":
        hien_thi = hien_thi[hien_thi["danh_muc"] == filter_dm]
    if filter_brand != "Tất cả":
        hien_thi = hien_thi[hien_thi["thuong_hieu"] == filter_brand]
    if search:
        hien_thi = hien_thi[hien_thi["ten_san_pham"].str.contains(search, case=False, na=False)]

    st.markdown(f"**Hiển thị {len(hien_thi)}/{len(sp_df)} sản phẩm**")

    # format lại cột giá để cho dễ đọc
    show = hien_thi.copy()
    show["gia_ban"]  = show["gia_ban"].apply(lambda x: f"{x:,.0f} đ")
    show["gia_nhap"] = show["gia_nhap"].apply(lambda x: f"{x:,.0f} đ")
    show = show.drop(columns=["mo_ta"], errors="ignore")
    st.dataframe(show, use_container_width=True, height=450)


def _tab_them_moi(sp_df):
    st.subheader("➕ Thêm sản phẩm mới")
    with st.form("form_them"):
        col1, col2 = st.columns(2)
        with col1:
            ma_moi       = st.text_input("Mã hàng *", placeholder="VD: DT011")
            ten_moi      = st.text_input("Tên sản phẩm *", placeholder="VD: iPhone 16 Pro 256GB")
            danh_muc_moi = st.selectbox("Danh mục *", DM_OPTIONS)
            brand_moi    = st.text_input("Thương hiệu *", placeholder="VD: Apple")
        with col2:
            gia_ban_moi  = st.number_input("Giá bán (VNĐ) *", min_value=0, step=10000)
            gia_nhap_moi = st.number_input("Giá nhập (VNĐ) *", min_value=0, step=10000)
            ton_kho_moi  = st.number_input("Tồn kho *", min_value=0, step=1)
            mo_ta_moi    = st.text_area("Mô tả", placeholder="Thông tin thêm...")

        if st.form_submit_button("💾 Lưu sản phẩm", type="primary"):
            if not ma_moi or not ten_moi:
                st.error("❌ Mã hàng và Tên sản phẩm không được để trống!")
            elif ma_moi in sp_df["ma_hang"].values:
                st.error(f"❌ Mã **{ma_moi}** đã tồn tại rồi!")
            elif gia_ban_moi < gia_nhap_moi:
                st.warning("⚠️ Giá bán thấp hơn giá nhập, kiểm tra lại!")
            else:
                dong_moi = {
                    "ma_hang": ma_moi, "ten_san_pham": ten_moi,
                    "danh_muc": danh_muc_moi, "thuong_hieu": brand_moi,
                    "gia_ban": gia_ban_moi, "gia_nhap": gia_nhap_moi,
                    "ton_kho": ton_kho_moi,
                    "mo_ta": mo_ta_moi or f"{ten_moi} - Hàng chính hãng, bảo hành 12 tháng",
                    "trang_thai": "Còn hàng" if ton_kho_moi > 10 else "Sắp hết hàng",
                }
                sp_df = pd.concat([sp_df, pd.DataFrame([dong_moi])], ignore_index=True)
                save_products(sp_df)
                st.success(f"✅ Đã thêm **{ten_moi}**!")
                st.rerun()


def _tab_sua_xoa(sp_df):
    st.subheader("✏️ Chỉnh sửa / Xóa sản phẩm")
    ma_chon = st.selectbox(
        "Chọn sản phẩm",
        sp_df["ma_hang"].tolist(),
        format_func=lambda x: f"{x} — {sp_df[sp_df['ma_hang']==x]['ten_san_pham'].values[0]}"
    )
    sp_chon = sp_df[sp_df["ma_hang"] == ma_chon].iloc[0]

    col_x1, col_x2 = st.columns([3, 1])
    with col_x1:
        with st.form("form_sua"):
            c1, c2 = st.columns(2)
            with c1:
                ten_sua   = st.text_input("Tên sản phẩm", value=sp_chon["ten_san_pham"])
                dm_idx    = DM_OPTIONS.index(sp_chon["danh_muc"]) if sp_chon["danh_muc"] in DM_OPTIONS else 0
                dm_sua    = st.selectbox("Danh mục", DM_OPTIONS, index=dm_idx)
                brand_sua = st.text_input("Thương hiệu", value=sp_chon["thuong_hieu"])
            with c2:
                gia_ban_sua  = st.number_input("Giá bán", value=int(sp_chon["gia_ban"]), step=10000)
                gia_nhap_sua = st.number_input("Giá nhập", value=int(sp_chon["gia_nhap"]), step=10000)
                ton_kho_sua  = st.number_input("Tồn kho", value=int(sp_chon["ton_kho"]), step=1)

            if st.form_submit_button("💾 Lưu thay đổi", type="primary"):
                idx = sp_df[sp_df["ma_hang"] == ma_chon].index[0]
                sp_df.at[idx, "ten_san_pham"] = ten_sua
                sp_df.at[idx, "danh_muc"]     = dm_sua
                sp_df.at[idx, "thuong_hieu"]  = brand_sua
                sp_df.at[idx, "gia_ban"]      = gia_ban_sua
                sp_df.at[idx, "gia_nhap"]     = gia_nhap_sua
                sp_df.at[idx, "ton_kho"]      = ton_kho_sua
                sp_df.at[idx, "trang_thai"]   = "Còn hàng" if ton_kho_sua > 10 else "Sắp hết hàng"
                save_products(sp_df)
                st.success("✅ Cập nhật thành công!")
                st.rerun()

    with col_x2:
        st.markdown("### ⚠️ Xóa")
        st.warning(f"Xóa: **{sp_chon['ten_san_pham']}**")
        if st.button("🗑️ Xóa sản phẩm", type="secondary"):
            sp_df = sp_df[sp_df["ma_hang"] != ma_chon]
            save_products(sp_df)
            st.success("✅ Đã xóa!")
            st.rerun()
