import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cấu hình cài đặt phông chữ Times New Roman cho Matplotlib (Biểu đồ)
plt.rcParams["font.family"] = "Times New Roman"

# Cấu hình trang với layout wide
st.set_page_config(page_title="Ứng dụng tính khoản vay", layout="wide")

# =========================================================================
# CSS ÉP GIAO DIỆN SÁNG (XÓA Ô ĐEN) & ĐỒNG BỘ PHÔNG CHỮ TIMES NEW ROMAN
# =========================================================================
st.markdown("""
<style>
    /* 1. ÉP PHÔNG CHỮ TIMES NEW ROMAN CHO TOÀN BỘ ỨNG DỤNG */
    * {
        font-family: 'Times New Roman', Times, serif !important;
    }
    
    /* 2. CHUYỂN TOÀN BỘ CHỮ SANG MÀU TỐI ĐỂ NỔI TRÊN NỀN SÁNG */
    h1, h2, h3, h4, h5, h6, p, span, label, li, td, th {
        color: #1e293b !important;
    }

    /* 3. NỀN TRANG WEB SÁNG DỊU MẮT */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
    }

    /* Tiêu đề chính */
    .main-title {
        color: #0f172a !important;
        text-align: center;
        margin-bottom: 30px;
        font-size: 34px !important;
        font-weight: 800 !important;
    }

    /* 4. CHỈNH Ô NHẬP SỐ (NUMBER INPUT) THÀNH MÀU TRẮNG */
    div[data-baseweb="input"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="input"] input {
        background-color: #ffffff !important;
        color: #1e293b !important;
    }
    /* Nút tăng/giảm số (+/-) */
    div[data-baseweb="input"] button {
        background-color: #f1f5f9 !important;
        color: #1e293b !important;
        border: none !important;
    }

    /* 5. CHỈNH Ô CHỌN (SELECTBOX) THÀNH MÀU TRẮNG */
    div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #1e293b !important;
    }
    div[data-baseweb="select"] span {
        color: #1e293b !important;
    }
    /* Biểu tượng mũi tên trỏ xuống */
    div[data-baseweb="select"] svg {
        fill: #1e293b !important;
    }

    /* Đổi màu menu danh sách lựa chọn khi click mở Selectbox */
    div[role="listbox"] {
        background-color: #ffffff !important;
    }
    div[role="listbox"] * {
        color: #1e293b !important;
        background-color: #ffffff !important;
    }

    /* 6. CHỈNH THANH TRƯỢT (SLIDER) */
    div[data-testid="stSlider"] * {
        color: #1e293b !important;
    }

    /* 7. CHỈNH ĐẦU BẢNG (TABLE HEADER) THÀNH MÀU TRẮNG/XÁM SÁNG */
    .stTable table {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-collapse: collapse !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    .stTable th {
        background-color: #f1f5f9 !important; /* Đổi đầu bảng từ đen sang xám trắng */
        color: #0f172a !important; /* Chữ màu đen sẫm dễ nhìn */
        font-weight: bold !important;
        border-bottom: 2px solid #cbd5e1 !important;
        padding: 12px !important;
    }
    .stTable td {
        background-color: #ffffff !important;
        color: #334155 !important;
        border-bottom: 1px solid #e2e8f0 !important;
        padding: 12px !important;
    }

    /* 8. THIẾT KẾ CONTAINER CARD TRẮNG BO TRÒN */
    .input-card, .result-card {
        background-color: #ffffff !important;
        border-radius: 16px !important;
        padding: 25px !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05) !important;
        margin-bottom: 25px !important;
    }
    
    .result-card .label {
        font-size: 15px !important;
        color: #64748b !important;
        font-weight: bold !important;
    }
    
    .result-card .value {
        font-size: 26px !important;
        font-weight: bold !important;
        color: #0284c7 !important;
    }

    /* Khung tư vấn */
    .advice-card {
        background-color: #f0fdf4 !important;
        border: 1px solid #bbf7d0 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-top: 15px !important;
    }
    .advice-card .title {
        font-size: 18px !important;
        font-weight: bold !important;
        color: #166534 !important;
        margin-bottom: 10px !important;
    }
    .advice-card li {
        color: #15803d !important;
        font-size: 15px !important;
    }
</style>
""", unsafe_allow_html=True)

# Tiêu đề chính
st.markdown('<h1 class="main-title">🏦 ỨNG DỤNG TÍNH TOÁN KHOẢN VAY NGÂN HÀNG</h1>', unsafe_allow_html=True)

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

# Khung nhập thông tin vay
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

st.info(f"💡 Lãi suất áp dụng cho mục đích **{muc_dich}**: **{lai_nam}%/năm**")
st.markdown('</div>', unsafe_allow_html=True)

#==========================
# Tính toán
#==========================
thang = thoi_han * 12
lai_thang = lai_nam / 100 / 12

# PHƯƠNG THỨC 1: Dư nợ giảm dần
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
        round(goc_thang, 2),
        round(lai, 2),
        round(tong, 2),
        max(round(du_no, 2), 0)
    ])

df1 = pd.DataFrame(
    bang1,
    columns=["Tháng", "Gốc", "Lãi", "Thanh toán", "Dư nợ còn lại"]
)

# PHƯƠNG THỨC 2: Trả góp đều (Annuity)
A = so_tien * lai_thang * (1+lai_thang)**thang / ((1+lai_thang)**thang - 1)
du_no = so_tien
bang2 = []
tong_lai2 = 0

for i in range(1, thang + 1):
    lai = du_no * lai_thang
    goc = A - lai
    du_no -= goc
    tong_lai2 += lai
    bang2.append([
        i,
        round(goc, 2),
        round(lai, 2),
        round(A, 2),
        max(round(du_no, 2), 0)
    ])

df2 = pd.DataFrame(
    bang2,
    columns=["Tháng", "Gốc", "Lãi", "Thanh toán", "Dư nợ còn lại"]
)

#==========================
# SO SÁNH PHƯƠNG THỨC
#==========================
st.header("⚖️ SO SÁNH HAI PHƯƠNG THỨC TRẢ NỢ")

c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown('<h3>Phương án 1: Trả gốc đều - Lãi giảm dần</h3>', unsafe_allow_html=True)
    
    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown(f'<p class="label">Tổng tiền lãi</p><p class="value">{tong_lai1:,.2f} Tr</p>', unsafe_allow_html=True)
    with sc2:
        st.markdown(f'<p class="label">Tổng thanh toán</p><p class="value">{so_tien+tong_lai1:,.2f} Tr</p>', unsafe_allow_html=True)

    st.write("#### Lịch chi tiết trả nợ")
    st.dataframe(df1, height=300, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown('<h3>Phương án 2: Trả đều hàng tháng (Annuity)</h3>', unsafe_allow_html=True)
    
    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown(f'<p class="label">Tổng tiền lãi</p><p class="value">{tong_lai2:,.2f} Tr</p>', unsafe_allow_html=True)
    with sc2:
        st.markdown(f'<p class="label">Tổng thanh toán</p><p class="value">{so_tien+tong_lai2:,.2f} Tr</p>', unsafe_allow_html=True)

    st.write("#### Lịch chi tiết trả nợ")
    st.dataframe(df2, height=300, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

#==========================
# TỔNG PHẢI THANH TOÁN
#==========================
st.header("📋 BÁO CÁO PHÂN TÍCH TỔNG HỢP")

ss = pd.DataFrame({
    "Tiêu chí": ["Tổng lãi phải trả", "Tổng thanh toán (Gốc + Lãi)"],
    "Dư nợ giảm dần (PA 1)": [f"{tong_lai1:,.2f} triệu", f"{so_tien+tong_lai1:,.2f} triệu"],
    "Trả đều hàng tháng (PA 2)": [f"{tong_lai2:,.2f} triệu", f"{so_tien+tong_lai2:,.2f} triệu"]
})

st.markdown('<div class="result-card">', unsafe_allow_html=True)
st.table(ss)

# Phần gợi ý tư vấn động dựa trên kết quả tính toán
if tong_lai1 < tong_lai2:
    st.markdown(f"""
<div class="advice-card">
    <div class="title">💡 GỢI Ý TỪ CỐ VẤN TÀI CHÍNH</div>
    <ul>
        <li>✔ Bạn nên chọn <b>Phương án 1 (Dư nợ giảm dần)</b> để tiết kiệm được khoảng <b>{(tong_lai2 - tong_lai1):,.2f} triệu đồng</b> tiền lãi.</li>
        <li>✔ Phương án này cực kỳ tối ưu nếu bạn có nguồn thu nhập ổn định và dư dả trong thời gian đầu.</li>
        <li>✔ Dư nợ gốc giảm nhanh giúp giảm áp lực lãi suất về sau.</li>
    </ul>
</div>
""", unsafe_allow_html=True)
else:
    st.markdown(f"""
<div class="advice-card" style="background-color: #eff6ff !important; border-color: #bfdbfe !important;">
    <div class="title" style="color: #1e40af !important;">💡 GỢI Ý TỪ CỐ VẤN TÀI CHÍNH</div>
    <ul style="color: #1e3a8a !important;">
        <li>✔ Bạn nên chọn <b>Phương án 2 (Trả đều hàng tháng)</b>.</li>
        <li>✔ Số tiền trả cố định giúp bạn dễ dàng lập kế hoạch chi tiêu hàng tháng mà không lo biến động tài chính.</li>
        <li>✔ Rất phù hợp cho người đi làm hưởng lương cố định.</li>
    </ul>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

#==========================
# BIỂU ĐỒ CỘT THEO NĂM
#==========================
st.header("📉 BIỂU ĐỒ DƯ NỢ CÒN LẠI THEO NĂM")

# Lấy số dư nợ cuối mỗi năm
df_nam = df1[df1["Tháng"] % 12 == 0].copy()
if df1.iloc[-1]["Tháng"] % 12 != 0:
    df_nam = pd.concat([df_nam, df1.tail(1)])

nam = [f"Năm {i+1}" for i in range(len(df_nam))]
du_no = df_nam["Dư nợ còn lại"].values

fig, ax = plt.subplots(figsize=(10, 4.5))
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#ffffff')

# Thiết kế cột biểu đồ hiện đại
bars = ax.bar(
    nam,
    du_no,
    color="#0284c7", # Màu xanh dương chuyên nghiệp
    edgecolor="#0284c7",
    width=0.55,
    alpha=0.9
)

# Hiển thị số liệu trực quan trên cột
for bar in bars:
    h = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width()/2,
        h + (so_tien * 0.02),
        f"{h:.1f} Tr",
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold",
        color="#334155"
    )

ax.set_title("Số tiền dư nợ còn lại qua từng năm (Phương án 1)", fontsize=13, fontweight="bold", color="#0f172a", pad=15)
ax.set_ylabel("Triệu đồng", fontsize=10, color="#475569")
ax.grid(axis="y", linestyle="--", alpha=0.3)

# Làm mượt các đường biên của biểu đồ
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#cbd5e1")
ax.spines["bottom"].set_color("#cbd5e1")
ax.tick_params(colors="#475569")

# Đưa biểu đồ vào khung kết quả sáng
st.markdown('<div class="result-card">', unsafe_allow_html=True)
st.pyplot(fig)
st.markdown('</div>', unsafe_allow_html=True)
