import streamlit as st
import pandas as pd
import io
from utils.style import page_header


def show(products_df, orders_df):
    page_header("📤 Xuất Báo cáo", "Tải dữ liệu ra file Excel hoặc CSV")

    st.info("Chọn loại báo cáo và định dạng bên dưới rồi bấm tải.")

    loai_bc = st.selectbox("📁 Loại báo cáo", [
        "Danh sách sản phẩm",
        "Tất cả đơn hàng",
        "Đơn hàng hoàn thành",
        "Tổng hợp doanh thu theo danh mục",
        "Tổng hợp doanh thu theo tháng",
        "Top 10 sản phẩm bán chạy",
    ])

    dinh_dang = st.radio("📄 Định dạng", ["Excel (.xlsx)", "CSV (.csv)"], horizontal=True)

    if st.button("⬇️ Tạo & Tải xuống", type="primary"):
        data_xuat = _tao_bao_cao(loai_bc, products_df, orders_df)
        ten_file  = loai_bc.replace(" ", "_").replace("/", "-")

        if dinh_dang == "Excel (.xlsx)":
            raw = _xuat_excel(data_xuat)
            st.download_button("📥 Tải file Excel", data=raw,
                               file_name=f"{ten_file}.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            csv_str = data_xuat.to_csv(index=False, encoding="utf-8-sig")
            st.download_button("📥 Tải file CSV", data=csv_str,
                               file_name=f"{ten_file}.csv", mime="text/csv")

        st.success(f"✅ Báo cáo **{loai_bc}** đã sẵn sàng!")
        st.dataframe(data_xuat, use_container_width=True)


def _tao_bao_cao(loai_bc: str, products_df, orders_df) -> pd.DataFrame:
    don_ht = orders_df[orders_df["trang_thai_don"] == "Hoàn thành"]

    if loai_bc == "Danh sách sản phẩm":
        return products_df.copy()

    elif loai_bc == "Tất cả đơn hàng":
        return orders_df.drop(columns=["thang", "quy", "loi_nhuan"], errors="ignore")

    elif loai_bc == "Đơn hàng hoàn thành":
        return don_ht.drop(columns=["thang", "quy", "loi_nhuan"], errors="ignore")

    elif loai_bc == "Tổng hợp doanh thu theo danh mục":
        df = don_ht.groupby("danh_muc").agg(
            so_don=("ma_don_hang", "count"),
            so_luong_ban=("so_luong", "sum"),
            doanh_thu=("thanh_tien", "sum"),
            loi_nhuan=("loi_nhuan", "sum"),
        ).reset_index()
        df.columns = ["Danh mục", "Số đơn", "Số lượng bán", "Doanh thu (đ)", "Lợi nhuận (đ)"]
        return df

    elif loai_bc == "Tổng hợp doanh thu theo tháng":
        df = don_ht.groupby("thang").agg(
            so_don=("ma_don_hang", "count"),
            doanh_thu=("thanh_tien", "sum"),
            loi_nhuan=("loi_nhuan", "sum"),
        ).reset_index()
        df.columns = ["Tháng", "Số đơn", "Doanh thu (đ)", "Lợi nhuận (đ)"]
        return df
    
    #Top 10 all
    else:
        df = (don_ht.groupby("ten_san_pham").agg(
            danh_muc=("danh_muc", "first"),
            so_luong=("so_luong", "sum"),
            doanh_thu=("thanh_tien", "sum"),
        ).sort_values("so_luong", ascending=False).head(10).reset_index())
        df.columns = ["Sản phẩm", "Danh mục", "Số lượng bán", "Doanh thu (đ)"]
        return df


def _xuat_excel(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="BaoCao", index=False)
    return buf.getvalue()
