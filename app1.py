import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cấu hình trang với layout wide
st.set_page_config(page_title="Ứng dụng tính khoản vay", layout="wide")

# CSS tùy chỉnh để làm đẹp giao diện, học hỏi kiểu dáng từ image_0.png
st.markdown("""
<style>
    /* Tổng thể trang */
    [data-testid="stAppViewContainer"] {
        background-color: #f9f9fb; /* Nền nhạt */
    }

    /* Tiêu đề chính */
    .main-title {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 30px;
        font-size: 36px !important;
        font-weight: bold !important;
    }

    /* Thẻ input */
    .input-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #ddd;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* Thẻ kết quả (nhỏ) */
    .result-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #ddd;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        text-align: center;
    }
    .result-card .label {
        font-size: 14px;
        color: #777;
        margin-bottom: 5px;
    }
    .result-card .value {
        font-size: 24px;
        font-weight: bold;
        color: #007bff; /* Màu xanh nhấn */
        margin-bottom: 0px;
    }

    /* Thẻ tư vấn */
    .advice-card {
        background-color: #e3f2fd; /* Màu xanh nhạt */
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #90caf9;
        margin-bottom: 20px;
    }
    .advice-card .title {
        font-size: 18px;
        font-weight: bold;
        color: #1976d2;
        margin-bottom: 10px;
    }
    .advice-card ul {
        list-style-type: none;
        padding: 0;
        margin: 0;
    }
    .advice-card li {
        color: #1565c0;
        margin-bottom: 5px;
        font-size: 16px;
    }

    /* Nút */
    .stButton>button {
        background-color: #007bff !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
    }

    /* Bảng dữ liệu */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Tiêu đề chính
st.markdown('<h1 class="main-title">💰 ỨNG DỤNG TÍNH TOÁN TIỀN VAY NGÂN HÀNG</h1>', unsafe_allow_html=True)

# ==========================
# Lãi suất theo mục đích vay
# ==========================

lai_suat = {
    "Mua nhà": 7.5,
    "Mua ô tô": 8.5,
    "Kinh doanh": 10,
    "Tiêu dùng": 12,
    "Du học": 9
}

# Vùng nhập thông tin được đặt trong thẻ
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.write("### 📝 Nhập thông tin kế hoạch vay")

col1, col2 = st.columns(2)

with col1:
    so_tien = st.number_input(
        "Số tiền vay (triệu đồng)",
        min_value=1.0,
        value=500.0,
        step=10.0
    )

    muc_dich = st.selectbox(
        "Mục đích vay",
        list(lai_suat.keys())
    )

with col2:
    thoi_han = st.slider(
        "Thời hạn vay (năm)",
        1,
        30,
        10
    )

    lai_nam = lai_suat[muc_dich]

st.success(f"Lãi suất áp dụng: **{lai_nam}%/năm**")
st.markdown('</div>', unsafe_allow_html=True)

#==========================
# Tính toán
#==========================

thang = thoi_han * 12
lai_thang = lai_nam / 100 / 12

#==========================
# PHƯƠNG THỨC 1
# Dư nợ giảm dần
#==========================

goc_thang = so_tien / thang
du_no = so_tien
bang1 = []
tong_lai1 = 0

for i in range(1, thang + 1):
    lai = du_no * lai_thang
    tong = goc_thang + lai
    du_no -= goc_thang
    tong_lai1 += lai
    bang1.append([
        i,
        round(goc_thang,2),
        round(lai,2),
        round(tong,2),
        max(round(du_no,2),0)
    ])

df1 = pd.DataFrame(
    bang1,
    columns=[
        "Tháng",
        "Gốc",
        "Lãi",
        "Thanh toán",
        "Dư nợ còn lại"
    ]
)

#==========================
# PHƯƠNG THỨC 2
# Trả góp đều (Annuity)
#==========================

A = so_tien * lai_thang * (1+lai_thang)**thang / ((1+lai_thang)**thang -1)
du_no = so_tien
bang2=[]
tong_lai2=0

for i in range(1,thang+1):
    lai=du_no*lai_thang
    goc=A-lai
    du_no-=goc
    tong_lai2+=lai
    bang2.append([
        i,
        round(goc,2),
        round(lai,2),
        round(A,2),
        max(round(du_no,2),0)
    ])

df2=pd.DataFrame(
    bang2,
    columns=[
        "Tháng",
        "Gốc",
        "Lãi",
        "Thanh toán",
        "Dư nợ còn lại"
    ]
)

#==========================
# SO SÁNH PHƯƠNG THỨC
#==========================

st.header("📊 SO SÁNH CÁC PHƯƠNG THỨC TRẢ NỢ")

c1,c2=st.columns(2)

with c1:
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.subheader("Phương thức 1")
    st.write("### Trả gốc đều - lãi giảm dần")

    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown(f'<p class="label">Tổng tiền lãi</p><p class="value">{tong_lai1:,.2f} Tr</p>', unsafe_allow_html=True)
    with sc2:
        st.markdown(f'<p class="label">Tổng thanh toán</p><p class="value">{so_tien+tong_lai1:,.2f} Tr</p>', unsafe_allow_html=True)

    st.dataframe(df1,height=350, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.subheader("Phương thức 2")
    st.write("### Trả đều hàng tháng (Annuity)")

    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown(f'<p class="label">Tổng tiền lãi</p><p class="value">{tong_lai2:,.2f} Tr</p>', unsafe_allow_html=True)
    with sc2:
        st.markdown(f'<p class="label">Tổng thanh toán</p><p class="value">{so_tien+tong_lai2:,.2f} Tr</p>', unsafe_allow_html=True)

    st.dataframe(df2,height=350, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

#==========================
# TỔNG PHẢI THANH TOÁN
#==========================

st.header("📋 BÁO CÁO TỔNG QUAN")

ss = pd.DataFrame({
    "Tiêu chí":[
        "Tổng lãi",
        "Tổng thanh toán"
    ],
    "Dư nợ giảm dần":[
        round(tong_lai1,2),
        round(so_tien+tong_lai1,2)
    ],
    "Trả đều":[
        round(tong_lai2,2),
        round(so_tien+tong_lai2,2)
    ]
})

# Đặt bảng tổng hợp trong container có viền bo tròn
st.markdown('<div class="result-card">', unsafe_allow_html=True)
st.table(ss)
st.markdown('</div>', unsafe_allow_html=True)

#==========================
# TƯ VẤN (Sử dụng thẻ tư vấn tùy chỉnh)
#==========================

st.markdown('<div class="result-card">', unsafe_allow_html=True)
st.write("### 💡 Gợi ý tư vấn")
if tong_lai1 < tong_lai2:
    st.markdown("""
<div class="advice-card">
    <div class="title">Tư vấn: Nên chọn phương thức trả gốc đều (dư nợ giảm dần)</div>
    <ul>
        <li>✔ Tổng lãi thấp hơn, tiết kiệm chi phí.</li>
        <li>✔ Khoản trả giảm dần qua từng tháng.</li>
        <li>✔ Phù hợp nếu bạn có thu nhập cao ban đầu.</li>
    </ul>
</div>
""", unsafe_allow_html=True)
else:
    st.markdown("""
<div class="advice-card">
    <div class="title">Tư vấn: Nên chọn phương thức trả đều hàng tháng (Annuity)</div>
    <ul>
        <li>✔ Khoản trả cố định, dễ dàng cân đối tài chính.</li>
        <li>✔ Không gặp áp lực cao ở những tháng đầu.</li>
        <li>✔ Phù hợp nếu bạn có thu nhập ổn định.</li>
    </ul>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

#==========================
# BIỂU ĐỒ CỘT THEO NĂM
#==========================

st.header("📉 ĐỒ THỊ DƯ NỢ CÒN LẠI THEO NĂM")

# Lấy số dư nợ cuối mỗi năm
df_nam = df1[df1["Tháng"] % 12 == 0].copy()

# Nếu năm cuối chưa đủ 12 tháng thì vẫn lấy
if df1.iloc[-1]["Tháng"] % 12 != 0:
    df_nam = pd.concat([df_nam, df1.tail(1)])

# Tạo tên năm
nam = [f"Năm {i+1}" for i in range(len(df_nam))]
du_no = df_nam["Dư nợ còn lại"].values

fig, ax = plt.subplots(figsize=(10,5))
fig.patch.set_facecolor('#ffffff') # Màu nền của toàn bộ biểu đồ

# Màu cột và kiểu dáng
bars = ax.bar(
    nam,
    du_no,
    color="#2e7d32", # Màu xanh lá đậm hơn, sạch hơn
    edgecolor="black",
    width=0.6,
    linewidth=0.5
)

# Hiển thị số trên đầu cột với định dạng triệu
for bar in bars:
    h = bar.get_height()
    ax.text(
        bar.get_x()+bar.get_width()/2,
        h+10, # Khoảng cách cao hơn
        f"{h:.1f} Tr", # Thêm "Tr"
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold",
        color="#2c3e50"
    )

# Tiêu đề biểu đồ
ax.set_title(
    "Số tiền còn lại phải trả theo từng năm",
    fontsize=14,
    fontweight="bold",
    color="#2c3e50",
    pad=20
)

# Tên trục
ax.set_ylabel("Triệu đồng", fontsize=12, color="#2c3e50")
ax.set_xlabel("", fontsize=12, color="#2c3e50")

# Đường lưới ngang giống Excel
ax.grid(axis="y", linestyle="--", alpha=0.5)

# Ẩn 2 cạnh trên và phải
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Đặt biểu đồ Matplotlib vào một thẻ container
st.markdown('<div class="result-card">', unsafe_allow_html=True)
st.pyplot(fig)
st.markdown('</div>', unsafe_allow_html=True)
