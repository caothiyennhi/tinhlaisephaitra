import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cấu hình cài đặt phông chữ Times New Roman cho Matplotlib (Biểu đồ)
plt.rcParams["font.family"] = "Times New Roman"

# Cấu hình trang với layout wide
st.set_page_config(page_title="Ứng dụng tính khoản vay", layout="wide")

# =========================================================================
# CSS ÉP GIAO DIỆN SÁNG, CHỮ ĐEN, Ô NHẬP TRẮNG & KẺ LƯỚI BẢNG 3X3 ĐEN ĐẬM
# =========================================================================
st.markdown("""
<style>
    /* 1. ĐỒNG BỘ PHÔNG CHỮ TIMES NEW ROMAN TOÀN CẦU */
    * {
        font-family: 'Times New Roman', Times, serif !important;
    }
    
    /* Ép toàn bộ chữ hiển thị trên trang thành màu đen */
    h1, h2, h3, h4, h5, h6, p, span, label, li, td, th, input {
        color: #000000 !important;
    }

    /* Nền trang web sáng nhẹ nhàng */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
    }

    /* Tiêu đề chính */
    .main-title {
        color: #000000 !important;
        text-align: center;
        margin-bottom: 30px;
        font-size: 34px !important;
        font-weight: bold !important;
    }

    /* 2. ÉP Ô NHẬP SỐ (NUMBER INPUT) THÀNH TRẮNG, CHỮ ĐEN */
    div[data-testid="stNumberInput"] div {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    div[data-testid="stNumberInput"] input {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    /* Các nút cộng / trừ (+ / -) bên cạnh ô nhập số */
    div[data-testid="stNumberInput"] button {
        background-color: #f1f5f9 !important;
        color: #000000 !important;
        border: 1px solid #cbd5e1 !important;
    }

    /* 1. Chuyển nền khung ngoài của Selectbox thành màu trắng */
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important; /* Viền xám nhạt cho đẹp */
    border-radius: 8px !important;
}

/* 2. Chuyển nền của các ô chứa chữ bên trong thành màu trắng và chữ màu đen */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #000000 !important;
}

/* 3. Ép chữ hiển thị của lựa chọn đang chọn (ví dụ: "Mua nhà") thành màu đen */
div[data-testid="stSelectbox"] span {
    color: #000000 !important;
}

/* 4. Đổi màu biểu tượng mũi tên trỏ xuống thành màu đen */
div[data-testid="stSelectbox"] svg {
    fill: #000000 !important;
}

/* 5. Chỉnh luôn cả danh sách lựa chọn khi bấm click mở ô ra (nền trắng, chữ đen) */
div[role="listbox"], ul[role="listbox"] {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
}
div[role="listbox"] li, ul[role="listbox"] li {
    background-color: #ffffff !important;
    color: #000000 !important;
}
/* Hiệu ứng khi di chuột qua các dòng lựa chọn */
div[role="listbox"] li:hover, ul[role="listbox"] li:hover {
    background-color: #f1f5f9 !important;
}

    /* 4. CHỈNH KHUNG BẢNG TỔNG HỢP THÀNH LƯỚI 3X3 CÓ GẠCH CHIA Ô MÀU ĐEN RÕ RÀNG */
    .stTable table {
        background-color: #ffffff !important;
        border: 2px solid #000000 !important; /* Viền ngoài màu đen */
        border-collapse: collapse !important;
        width: 100% !important;
    }
    .stTable th {
        background-color: #f1f5f9 !important; /* Nền tiêu đề xám nhẹ */
        color: #000000 !important;
        font-weight: bold !important;
        border: 2px solid #000000 !important; /* Gạch phân tách cột tiêu đề màu đen */
        padding: 12px !important;
        text-align: left !important;
    }
    .stTable td {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #000000 !important; /* Gạch ngang/dọc chia các ô thành lưới 3x3 màu đen rõ rệt */
        padding: 12px !important;
        text-align: left !important;
    }

    /* 5. ĐỒNG BỘ CÁC NỀN KHUNG CONTAINER SÁNG TRẮNG ĐẸP MẮT (BẢN ĐỊA STREAMLIT) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05) !important;
        padding: 20px !important;
    }
    
    .result-label {
        font-size: 15px !important;
        color: #475569 !important;
        font-weight: bold !important;
    }
    
    .result-value {
        font-size: 26px !important;
        font-weight: bold !important;
        color: #0284c7 !important;
    }

    /* Khung gợi ý tư vấn màu xanh lá nhạt dịu */
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

# Khung nhập thông tin vay (sử dụng container bản địa tránh lỗi ô trắng trống)
with st.container(border=True):
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

#==========================
# Tính toán các phương án
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
    with st.container(border=True):
        st.markdown('### Phương án 1: Trả gốc đều - Lãi giảm dần')
        
        sc1, sc2 = st.columns(2)
        with sc1:
            st.markdown(f'<p class="result-label">Tổng tiền lãi</p><p class="result-value">{tong_lai1:,.2f} Tr</p>', unsafe_allow_html=True)
        with sc2:
            st.markdown(f'<p class="result-label">Tổng thanh toán</p><p class="result-value">{so_tien+tong_lai1:,.2f} Tr</p>', unsafe_allow_html=True)

        st.write("#### Lịch chi tiết trả nợ")
        st.dataframe(df1, height=300, use_container_width=True)

with c2:
    with st.container(border=True):
        st.markdown('### Phương án 2: Trả đều hàng tháng (Annuity)')
        
        sc1, sc2 = st.columns(2)
        with sc1:
            st.markdown(f'<p class="result-label">Tổng tiền lãi</p><p class="result-value">{tong_lai2:,.2f} Tr</p>', unsafe_allow_html=True)
        with sc2:
            st.markdown(f'<p class="result-label">Tổng thanh toán</p><p class="result-value">{so_tien+tong_lai2:,.2f} Tr</p>', unsafe_allow_html=True)

        st.write("#### Lịch chi tiết trả nợ")
        st.dataframe(df2, height=300, use_container_width=True)

#==========================
# TỔNG PHẢI THANH TOÁN (LƯỚI 3X3)
#==========================
st.header("📋 BÁO CÁO PHÂN TÍCH TỔNG HỢP")

# Xây dựng bảng 3x3 rõ nét (bao gồm 1 hàng tiêu đề và 2 hàng dữ liệu, chia 3 cột)
ss = pd.DataFrame({
    "Tiêu chí": ["Tổng lãi phải trả", "Tổng thanh toán (Gốc + Lãi)"],
    "Dư nợ giảm dần (PA 1)": [f"{tong_lai1:,.2f} triệu", f"{so_tien+tong_lai1:,.2f} triệu"],
    "Trả đều hàng tháng (PA 2)": [f"{tong_lai2:,.2f} triệu", f"{so_tien+tong_lai2:,.2f} triệu"]
})

with st.container(border=True):
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

# Đưa biểu đồ vào khung kết quả sáng bản địa
with st.container(border=True):
    st.pyplot(fig)
