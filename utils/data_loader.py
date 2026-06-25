import pandas as pd
import os
import streamlit as st

#Link dẫn gốc của project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PRODUCTS_PATH = os.path.join(BASE_DIR, "products.csv")
ORDERS_PATH   = os.path.join(BASE_DIR, "orders.csv")


@st.cache_data
def load_data():
    products = pd.read_csv(PRODUCTS_PATH)
    orders   = pd.read_csv(ORDERS_PATH)

    orders["ngay_dat"] = pd.to_datetime(orders["ngay_dat"])
    orders["thang"] = orders["ngay_dat"].dt.month
    orders["quy"]   = orders["ngay_dat"].dt.quarter

    # lợi nhuận từng dòng = (giá bán - giá nhập) * số lượng
    orders["loi_nhuan"] = orders.apply(
        lambda r: (r["don_gia"] - products.loc[
            products["ma_hang"] == r["ma_hang"], "gia_nhap"
        ].values[0]) * r["so_luong"] if r["ma_hang"] in products["ma_hang"].values else 0,
        axis=1
    )
    return products, orders


# Không cache vì cần đọc bản mới nhất sau khi thêm, sửa, xóa
def reload_products():
    return pd.read_csv(PRODUCTS_PATH)


def save_products(df: pd.DataFrame):
    df.to_csv(PRODUCTS_PATH, index=False, encoding="utf-8")
