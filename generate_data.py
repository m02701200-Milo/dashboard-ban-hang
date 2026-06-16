import csv
import random
from datetime import datetime, timedelta

# Danh sách sản phẩm điện tử, âm thanh

san_pham = [
    # ---- ĐIỆN THOẠI ---
    ("DT001", "iPhone 15 Pro Max 256GB", "Điện thoại", "Apple", 34990000, 28500000),
    ("DT002", "iPhone 15 128GB", "Điện thoại", "Apple", 22990000, 18000000),
    ("DT003", "Samsung Galaxy S24 Ultra", "Điện thoại", "Samsung", 31990000, 25000000),
    ("DT004", "Samsung Galaxy A55 5G", "Điện thoại", "Samsung", 10490000, 7800000),
    ("DT005", "Xiaomi 14 Pro", "Điện thoại", "Xiaomi", 18990000, 14500000),
    ("DT006", "Xiaomi Redmi Note 13 Pro", "Điện thoại", "Xiaomi", 7490000, 5200000),
    ("DT007", "OPPO Reno 11 Pro 5G", "Điện thoại", "OPPO", 12990000, 9500000),
    ("DT008", "Vivo V30 Pro", "Điện thoại", "Vivo", 11490000, 8200000),
    ("DT009", "Google Pixel 8 Pro", "Điện thoại", "Google", 27990000, 21000000),
    ("DT010", "OnePlus 12 5G", "Điện thoại", "OnePlus", 19990000, 15000000),

    # --- TAI NGHE -----
    ("TN001", "Sony WH-1000XM5 Wireless", "Tai nghe", "Sony", 8490000, 5800000),
    ("TN002", "Apple AirPods Pro 2nd Gen", "Tai nghe", "Apple", 6490000, 4500000),
    ("TN003", "Bose QuietComfort 45", "Tai nghe", "Bose", 7990000, 5600000),
    ("TN004", "Samsung Galaxy Buds2 Pro", "Tai nghe", "Samsung", 4490000, 2900000),
    ("TN005", "JBL Tune 770NC", "Tai nghe", "JBL", 2290000, 1400000),
    ("TN006", "Sennheiser Momentum 4", "Tai nghe", "Sennheiser", 9990000, 7200000),
    ("TN007", "Jabra Evolve2 75", "Tai nghe", "Jabra", 12490000, 9000000),
    ("TN008", "Audio-Technica ATH-M50x", "Tai nghe", "Audio-Technica", 3990000, 2600000),
    ("TN009", "Anker Soundcore Life Q45", "Tai nghe", "Anker", 1490000, 890000),
    ("TN010", "Edifier W820NB Plus", "Tai nghe", "Edifier", 1990000, 1200000),
    ("TN011", "Sony WF-1000XM5 TWS", "Tai nghe", "Sony", 6990000, 4800000),
    ("TN012", "Nothing Ear (2)", "Tai nghe", "Nothing", 2990000, 1900000),

    # --- LOA ---
    ("LO001", "JBL Charge 5 Bluetooth", "Loa", "JBL", 3990000, 2600000),
    ("LO002", "Sony SRS-XB100", "Loa", "Sony", 1290000, 780000),
    ("LO003", "Bose SoundLink Max", "Loa", "Bose", 9490000, 6800000),
    ("LO004", "Marshall Emberton III", "Loa", "Marshall", 3490000, 2200000),
    ("LO005", "Harman Kardon Onyx Studio 8", "Loa", "Harman Kardon", 8990000, 6200000),
    ("LO006", "JBL Flip 6", "Loa", "JBL", 2490000, 1500000),
    ("LO007", "Sonos Era 100", "Loa", "Sonos", 7990000, 5500000),
    ("LO008", "Xiaomi Smart Speaker", "Loa", "Xiaomi", 990000, 580000),
    ("LO009", "Edifier R1280T Active", "Loa", "Edifier", 2190000, 1350000),
    ("LO010", "Bose TV Speaker", "Loa", "Bose", 5990000, 4000000),

    # --- TABLET ---
    ("TB001", "iPad Pro M4 11 inch 256GB", "Tablet", "Apple", 28990000, 22000000),
    ("TB002", "iPad Air M2 128GB", "Tablet", "Apple", 16990000, 12500000),
    ("TB003", "Samsung Galaxy Tab S9+", "Tablet", "Samsung", 22990000, 17000000),
    ("TB004", "Samsung Galaxy Tab A9+", "Tablet", "Samsung", 8490000, 5800000),
    ("TB005", "Xiaomi Pad 6 Pro", "Tablet", "Xiaomi", 10990000, 7800000),
    ("TB006", "Lenovo Tab P12 Pro", "Tablet", "Lenovo", 13990000, 10000000),

    # --- PHỤ KIỆN ---
    ("PK001", "Sạc nhanh Anker 65W GaN", "Phụ kiện", "Anker", 890000, 480000),
    ("PK002", "Cáp USB-C Belkin 2m", "Phụ kiện", "Belkin", 490000, 220000),
    ("PK003", "Ốp lưng Spigen iPhone 15 Pro", "Phụ kiện", "Spigen", 390000, 180000),
    ("PK004", "Kính cường lực Baseus iPhone 15", "Phụ kiện", "Baseus", 290000, 120000),
    ("PK005", "Pin dự phòng Anker 20000mAh", "Phụ kiện", "Anker", 1290000, 780000),
    ("PK006", "Giá đỡ điện thoại Ugreen", "Phụ kiện", "Ugreen", 290000, 130000),
    ("PK007", "Hub USB-C 7-in-1 Ugreen", "Phụ kiện", "Ugreen", 890000, 490000),
    ("PK008", "Bao da iPad Pro ESR", "Phụ kiện", "ESR", 590000, 280000),

    # --- ĐỒNG HỒ THÔNG MINH ---
    ("DH001", "Apple Watch Series 9 GPS 41mm", "Đồng hồ thông minh", "Apple", 10990000, 7800000),
    ("DH002", "Samsung Galaxy Watch 6 Classic", "Đồng hồ thông minh", "Samsung", 9490000, 6500000),
    ("DH003", "Garmin Venu 3", "Đồng hồ thông minh", "Garmin", 11990000, 8500000),
    ("DH004", "Xiaomi Watch S3", "Đồng hồ thông minh", "Xiaomi", 2990000, 1800000),
    ("DH005", "Fitbit Charge 6", "Đồng hồ thông minh", "Fitbit", 3490000, 2200000),
]


# Tạo file sản phẩm

with open("products.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow([
        "ma_hang", "ten_san_pham", "danh_muc", "thuong_hieu",
        "gia_ban", "gia_nhap", "ton_kho", "mo_ta", "trang_thai"
    ])
    for sp in san_pham:
        ma, ten, danh_muc, brand, gia_ban, gia_nhap = sp
        ton_kho = random.randint(5, 150)
        mo_ta = f"{ten} - Hàng chính hãng, bảo hành 12 tháng"
        trang_thai = "Còn hàng" if ton_kho > 10 else "Sắp hết hàng"
        writer.writerow([ma, ten, danh_muc, brand, gia_ban, gia_nhap, ton_kho, mo_ta, trang_thai])

print("✓ products.csv đã tạo xong")

# tạo file đơn hàng (500 đơn trong 12 tháng)

khach_hang = [
    "Nguyễn Văn An", "Trần Thị Bích", "Lê Minh Châu", "Phạm Thị Dung",
    "Hoàng Văn Em", "Vũ Thị Phương", "Đặng Minh Quân", "Bùi Thị Hoa",
    "Đỗ Văn Khoa", "Ngô Thị Lan", "Trịnh Văn Mạnh", "Lý Thị Ngọc",
    "Đinh Văn Phúc", "Hà Thị Quỳnh", "Cao Minh Sơn", "Mai Thị Trang",
    "Tô Văn Uy", "Lưu Thị Vân", "Phan Minh Xuân", "Kiều Thị Yến",
]

tinh_thanh = [
    "Hồ Chí Minh", "Hà Nội", "Đà Nẵng", "Cần Thơ",
    "Bình Dương", "Đồng Nai", "Long An", "Hải Phòng",
]

phuong_thuc = ["Tiền mặt", "Chuyển khoản", "Ví MoMo", "VNPay", "Thẻ tín dụng"]

start_date = datetime(2024, 1, 1)

with open("orders.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow([
        "ma_don_hang", "ngay_dat", "ma_hang", "ten_san_pham", "danh_muc",
        "khach_hang", "tinh_thanh", "so_luong", "don_gia",
        "thanh_tien", "phuong_thuc_tt", "trang_thai_don"
    ])

    trang_thai_don = ["Hoàn thành", "Hoàn thành", "Hoàn thành", "Đang xử lý", "Đã hủy"]

    for i in range(1, 601):
        sp = random.choice(san_pham)
        ma_sp, ten_sp, danh_muc, brand, gia_ban, gia_nhap = sp

        ngay = start_date + timedelta(days=random.randint(0, 364))
        so_luong = random.randint(1, 3)
        # giảm giá ngẫu nhiên 0-10%
        giam = random.uniform(0, 0.10)
        don_gia = int(gia_ban * (1 - giam))
        thanh_tien = don_gia * so_luong

        writer.writerow([
            f"DH{i:04d}",
            ngay.strftime("%Y-%m-%d"),
            ma_sp,
            ten_sp,
            danh_muc,
            random.choice(khach_hang),
            random.choice(tinh_thanh),
            so_luong,
            don_gia,
            thanh_tien,
            random.choice(phuong_thuc),
            random.choice(trang_thai_don),
        ])

print("✓ orders.csv đã tạo xong")
print(f"\nTổng: {len(san_pham)} sản phẩm, 600 đơn hàng")
