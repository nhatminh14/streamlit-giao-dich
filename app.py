import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard giao dịch",
    layout="wide"
)

st.title("Dashboard giao dịch thanh toán")

df = pd.read_excel(
    "digital_payment_fraud_shield_output.xlsx",
    sheet_name="predictions"
)
# Biểu đồ theo ngày
df["datetime"] = pd.to_datetime(df["datetime"])
# Tạo bộ lọc ở thanh bên trái
# Chọn mức rủi ro
muc_rui_ro = st.sidebar.selectbox(
    "Chọn mức rủi ro",
    ["Tất cả", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
)

# Lấy các kênh có trong dữ liệu
danh_sach_kenh = sorted(
    df["payment_channel"].dropna().unique().tolist()
)

kenh_thanh_toan = st.sidebar.selectbox(
    "Chọn kênh thanh toán",
    ["Tất cả"] + danh_sach_kenh
)

# Bắt đầu từ toàn bộ dữ liệu
df_loc = df.copy()

if muc_rui_ro != "Tất cả":
    df_loc = df_loc[
        df_loc["risk_level"] == muc_rui_ro
    ]

if kenh_thanh_toan != "Tất cả":
    df_loc = df_loc[
        df_loc["payment_channel"] == kenh_thanh_toan
    ]

tu_khoa = st.sidebar.text_input(
    "Tìm mã giao dịch hoặc khách hàng",
    placeholder="Ví dụ: TXN000540 hoặc CUST0001"
).strip()

if tu_khoa:
    khop_giao_dich = (
        df_loc["transaction_id"]
        .astype("string")
        .str.contains(tu_khoa, case=False, na=False, regex=False)
    )

    khop_khach_hang = (
        df_loc["customer_id"]
        .astype("string")
        .str.contains(tu_khoa, case=False, na=False, regex=False)
    )

    df_loc = df_loc[khop_giao_dich | khop_khach_hang]

# Tính các số tổng quan
tong_giao_dich = len(df_loc)
tong_so_tien = df_loc["amount"].sum()
so_canh_bao = (df_loc["predicted_fraud"] == 1).sum()
# Chia giao diện thành 3 cột
cot1, cot2, cot3 = st.columns(3)

cot1.metric("Tổng giao dịch", f"{tong_giao_dich:,}")
cot2.metric("Tổng số tiền (VND)", f"{tong_so_tien:,.0f}")
cot3.metric("Giao dịch bị gắn cờ", f"{so_canh_bao:,}")

st.dataframe(df_loc)



